const express = require('express');
const client = require('prom-client');

const app = express();
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['route', 'method', 'code'],
  buckets: [0.005,0.01,0.025,0.05,0.1,0.2,0.5,1,2,5]
});
register.registerMetric(httpDuration);

let CHAOS_FAIL_RATE = Number(process.env.CHAOS_FAIL_RATE || 0.05);    // 5% failures
let CHAOS_LATENCY_MS = Number(process.env.CHAOS_LATENCY_MS || 100);   // 100ms delay

function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

app.get('/', (_, res) => res.send('Aion app up ✅'));

app.get('/work', async (req, res) => {
  const start = process.hrtime();
  await sleep(CHAOS_LATENCY_MS + Math.floor(Math.random()*30));
  const fail = Math.random() < CHAOS_FAIL_RATE;
  const code = fail ? 500 : 200;
  res.status(code).send(fail ? 'boom 💥' : 'ok');

  const diff = process.hrtime(start);
  const seconds = diff[0] + diff[1]/1e9;
  httpDuration.labels('/work', 'GET', String(code)).observe(seconds);
});

app.get('/metrics', async (_, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.post('/admin/chaos', (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const f = url.searchParams.get('fail');
  const l = url.searchParams.get('latency');
  if (f !== null) CHAOS_FAIL_RATE = Math.max(0, Math.min(1, Number(f)));
  if (l !== null) CHAOS_LATENCY_MS = Math.max(0, Number(l));
  res.json({CHAOS_FAIL_RATE, CHAOS_LATENCY_MS});
});

const PORT = 8080;
app.listen(PORT, () => console.log(`Aion app on :${PORT}`));
