import subprocess
import logging

logger = logging.getLogger(__name__)

def helm_rollback(release: str, namespace: str) -> dict:
  cmd = [
    "helm", "rollback", release, 
    "-n", namespace,
    "--wait",
    "--timeout", "120s",
  ]

  logger.info(f"Running rollback: {' '.join(cmd)}")

  try: 
    result = subprocess.run(
      cmd, 
      capture_output=True,
      text=True,
      timeout=130,
    )

    if result.returncode == 0:
      logger.info(f"Rollback succeeded: {result.stdout.strip()}")
      return {"success": True, "message": result.stdout.strip()}
    else:
      logger.error(f"Rollback failed: {result.stderr.strip()}")
      return {"success": False, "message": result.stderr.strip()}

  except subprocess.TimeoutExpired:
    msg = "Rollback timed out after 130s"
    logger.error(msg)
    return {"success": False, "message": msg}
