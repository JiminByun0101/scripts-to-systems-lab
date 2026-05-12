from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time 
import random

app = FastAPI(title="RealSmile Payment Backend")

REQUEST_COUNT = Counter(
  "realsmile_requests_total",
  "Total Request Count",
  ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
  "realsmile_request_latency_seconds",
  "Request latency in seconds",
  ["endpoint"]
)

PAYMENT_FAILURES = Counter(
  "realsmile_payment_failures_total",
  "Total payment processing failures"
)

@app.get("/health")
def health():
  return {"status": "ok", "service": "realsmile-backend"}

@app.get("/metrics")
def metrics():
  return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/payment")
def process_payment():
  start = time.time()
  # Simulate occasional failures - gives Prometheus something real to scrape 
  if random.random() < 0.1:
    PAYMENT_FAILURES.inc()
    REQUEST_COUNT.labels("POST", "/payment", "500").inc()
    REQUEST_LATENCY.labels("/payment").observe(time.time() - start)
    return {"status": "error", "message": "payment processing failed"}, 500

  REQUEST_COUNT.labels("POST", "/payment", "200").inc()
  REQUEST_LATENCY.labels("/payment").observe(time.time() - start)
  return {"status": "ok", "message": "payment processed"}