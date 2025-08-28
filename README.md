
# 🚀 Aion: Self-Healing Chaos Engineering Platform

Hey everyone 👋, I’m **Harsh Kini**, an entry-level DevOps engineer who’s been on a mission to create something truly extraordinary.  
Aion is my experimental project where I tried to build a **self-healing system** that can watch itself, learn from failures, and automatically fix issues before humans even notice. 💡

---

## 🔥 Why I built Aion
I always believed DevOps is more than just CI/CD pipelines.  
In today’s world, systems face chaos every second – network failures, latency spikes, random crashes. Instead of waiting for humans to fix issues, why can’t the system **heal itself**?  

That’s exactly the idea behind **Aion**:  
👉 Introduce controlled chaos (failures, latency)  
👉 Continuously measure SLOs (latency, error rate)  
👉 Trigger **auto-remediation actions** to bring system back to life  

---

## 🛠 Tech Stack I Used
- **Docker** 🐳 → Containerized microservice app  
- **Python** 🐍 → Guardian (the brain that watches SLOs)  
- **Grafana k6** 📊 → Load & chaos testing  
- **Curl & Bash** → My best friends for debugging  
- **JSON Artifacts** → For recording baseline, chaos, recovery tests  

---

## ⚙️ How it Works (Storyline)
1. **Run the App** → Simple Node.js API with `/work` endpoint  
2. **Guardian Brain** → Python script keeps checking latency (p95), error %, RPS  
3. **Inject Chaos** → Adjust failure rate & latency knobs via `/admin/chaos`  
4. **Observe Behavior** → k6 loadtest simulates users, Guardian reacts in real time  
5. **Auto-Healing** → Guardian applies fixes (reduces chaos or resets conditions)  
6. **Artifacts Generated** → Baseline, chaos, and recovery performance reports  

---

## 🖼 Architecture Diagram
![Aion Architecture](./diagram/aion-architecture.png)

---

## 📸 Key Screenshots (For LinkedIn/GitHub)
Here are the important outputs I captured:  
- ✅ `guardian.py` showing **auto actions** (`[AION] ACTION set_chaos`)  
- ✅ `k6` performance results (`p95 latency`, error % under chaos)  
- ✅ Curl outputs proving chaos knobs are working (`CHAOS_FAIL_RATE`, `CHAOS_LATENCY_MS`)  
- ✅ Final `artifacts/*.json` files with baseline & recovery results  

---

## 🚀 How to Run (Step by Step)
```bash
# clone the repo
git clone https://github.com/HarshKini/aion.git
cd aion

# build the app
docker build -t aion-app ./app

# run the app
docker run -d --name aion-app -p 8080:8080 aion-app

# run the guardian brain
python3 monitor/guardian.py

# run loadtest
docker run --rm --network host -v "$(pwd)/k6:/scripts" grafana/k6 run /scripts/loadtest.js
```

---

## 💡 What I Learned
- How **chaos engineering** makes systems more resilient  
- Why **observability (p95, error rates, SLOs)** is critical  
- That DevOps is not just CI/CD – it’s about **building self-healing systems**  
- Most importantly → Even as a fresher, I can design projects that challenge real-world problems 🚀  

---

## 🏆 Final Words
This is just the **beginning of Aion**.  
I dream of extending it with **Kubernetes, Prometheus, and AI-based anomaly detection** in the future.  

If you’re reading this → Remember, innovation doesn’t need permission. 💯  
Thanks for checking out my project 🙏

— *Harsh Kini*
