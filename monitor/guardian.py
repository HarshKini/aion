import os, time, requests, subprocess

PROM = os.getenv("PROM", "http://localhost:9090")
APP  = os.getenv("APP",  "http://localhost:8080")
SLACK = os.getenv("SLACK_WEBHOOK", "")  # optional

def notify(msg):
    try:
        if SLACK:
            requests.post(SLACK, json={"text": msg}, timeout=3)
        print("[AION] " + msg)
    except Exception as e:
        print("Slack notify error:", e)

def q(expr):
    r = requests.get(f"{PROM}/api/v1/query", params={"query": expr}, timeout=5)
    r.raise_for_status()
    data = r.json()["data"]["result"]
    if not data: return 0.0
    return float(data[0]["value"][1])

def set_chaos(fail=None, latency=None):
    params = {}
    if fail is not None: params["fail"] = str(fail)
    if latency is not None: params["latency"] = str(latency)
    try:
        r = requests.post(f"{APP}/admin/chaos", params=params, timeout=3)
        notify(f"ACTION set_chaos -> {r.json()}")
    except Exception as e:
        notify(f"WARN set_chaos: {e}")

def maybe_aws_scale():
    # Optional: scale an Auto Scaling Group if envs are set
    ASG = os.getenv("AION_ASG_NAME", "")
    ENABLE = os.getenv("AION_ENABLE_AWS", "0") == "1"
    if not (ENABLE and ASG):
        return
    # Increase capacity by 1 (demo). Requires AWS CLI configured.
    try:
        # Get desired capacity
        out = subprocess.check_output(
            ["aws","autoscaling","describe-auto-scaling-groups","--auto-scaling-group-names",ASG,"--query","AutoScalingGroups[0].DesiredCapacity","--output","text"],
            text=True
        ).strip()
        desired = int(out) if out.isdigit() else 1
        new_desired = max(1, desired + 1)
        subprocess.check_call(["aws","autoscaling","set-desired-capacity","--auto-scaling-group-name",ASG,"--desired-capacity",str(new_desired),"--honor-cooldown"])
        notify(f"AWS ACTION: scaled ASG {ASG} from {desired} -> {new_desired}")
    except Exception as e:
        notify(f"AWS scale error (safe to ignore if not configured): {e}")

print("Aion Brain started. Watching SLOs…")
bad_streak = 0
while True:
    try:
        p95 = q('histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))') * 1000.0
        err = q('sum(rate(http_request_duration_seconds_count{code!~"2.."}[1m])) / sum(rate(http_request_duration_seconds_count[1m]))')
        rps = q('sum(rate(http_request_duration_seconds_count[1m]))')
        print(f"p95={p95:.1f}ms  err={err*100:.2f}%  rps={rps:.2f}")

        # Thresholds (tune freely)
        SLOW = p95 > 250
        ERROR = err > 0.02  # >2%

        if SLOW or ERROR:
            bad_streak += 1
        else:
            bad_streak = 0

        if bad_streak >= 2:
            # Fix aggressively
            set_chaos(fail=0.0, latency=50)
            maybe_aws_scale()
            bad_streak = 0
        else:
            # Healthy → allow small chaos to keep realism
            set_chaos(fail=0.03, latency=100)

    except Exception as e:
        notify(f"Guardian loop error: {e}")

    time.sleep(10)
