import logging
import os

from fastapi import FastAPI, Request, HTTPException
from rollback import helm_rollback

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s $(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="RealSmile Rollback Controller")

RELEASE_NAME = os.environ.get("HELM_RELEASE", "realsmile")
NAMESPACE = os.environ.get("HELM_NAMESPACE", "realsmile")
WATCHED_ALERT = "HighPaymentFailureRate"

@app.get("/health")
def health():
  return {"status": "ok", "service": "rollback-controller"}

@app.post("/webhook")
async def alertmanager_webhook(request: Request):
  payload = await request.json()

  alerts = payload.get("alerts", [])
  firing = [
    a for a in alerts
    if a.get("status") == "firing"
    and a.get("labels", {}).get("alertname") == WATCHED_ALERT
  ]

  if not firing:
    logger.info("Webhook received - no matching firing alerts, skipping")
    return {"status": "skipped", "reason": "no matching firing alerts"}

  alert = firing[0]
  logger.info(
    f"Alert firing: {alert['labels'].get('alertname')} | "
    f"severity={alert['labels'].get('severity')}"
    f"description={alert['annotations'].get('description', '')}"
  )

  result = helm_rollback(RELEASE_NAME, NAMESPACE)

  if result["success"]:
    logger.info(f"Rollback complete: release={RELEASE_NAME} namespace={NAMESPACE}")
    return {"status": "rolled_back", "release": RELEASE_NAME, "detail": result["message"]}
  else:
    logger.error(f"Rollback failed: {result['message']}")
    raise HTTPException(status_code=500, detail=result["message"])