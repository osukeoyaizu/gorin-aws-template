
# lambda_store_token_from_sqs.py
import json
import os
import time
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource("dynamodb").Table(os.environ["TOKEN_TABLE"])
TTL_DAYS = int(os.getenv("TTL_DAYS", "7"))
TTL_SECONDS = TTL_DAYS * 24 * 3600

def _extract_payload(body: str) -> dict:
    """
    CallbackStep -> SQS の body はそのまま JSON の場合と、
    SNS等でラップされていて body 内の 'Message' が JSON の場合がある。
    どちらにも耐性を持たせる。
    """
    try:
        p = json.loads(body)
    except json.JSONDecodeError:
        return {}

    if isinstance(p, dict) and "Message" in p:
        try:
            return json.loads(p["Message"])
        except Exception:
            return {}
    return p if isinstance(p, dict) else {}

def lambda_handler(event, context):
    stored = 0
    for r in event.get("Records", []):
        body = r.get("body") or ""
        payload = _extract_payload(body)
        token = payload.get("token")
        args = payload.get("arguments", {})
        model_pkg_arn = args.get("ModelPackageArn")

        if not token or not model_pkg_arn:
            logger.warning("Missing token or ModelPackageArn in message: %s", body)
            continue

        ddb.put_item(
            Item={
                "ModelPackageArn": model_pkg_arn,
                "CallbackToken": token,
                "ExpireAt": int(time.time()) + TTL_SECONDS,   # TTL属性（テーブル側でTTL有効化）
            }
        )
        stored += 1
        logger.info("Stored token for %s", model_pkg_arn)

    return {"stored": stored}
