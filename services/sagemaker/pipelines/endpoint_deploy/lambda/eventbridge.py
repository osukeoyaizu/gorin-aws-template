
# lambda_resume_on_model_approved.py
import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource("dynamodb").Table(os.environ["TOKEN_TABLE"])
sm = boto3.client("sagemaker")

def _resolve_latest_approved_arn_from_group(group_name: str) -> str | None:
    resp = sm.list_model_packages(
        ModelPackageGroupName=group_name,
        ModelApprovalStatus="Approved",
        SortBy="CreationTime",
        SortOrder="Descending",
        MaxResults=1,
    )
    items = resp.get("ModelPackageSummaryList", [])
    return items[0]["ModelPackageArn"] if items else None

def lambda_handler(event, context):
    # EventBridge (SageMaker Model Package State Change)
    detail = event.get("detail", {})
    if detail.get("ModelApprovalStatus") != "Approved":
        logger.info("Not Approved state; ignoring.")
        return {"skipped": True}

    model_pkg_arn = detail.get("ModelPackageArn") or detail.get("ModelPackageVersionArn")
    if not model_pkg_arn and "ModelPackageGroupName" in detail:
        model_pkg_arn = _resolve_latest_approved_arn_from_group(detail["ModelPackageGroupName"])

    if not model_pkg_arn:
        logger.error("Could not resolve ModelPackageArn from event: %s", json.dumps(event))
        return {"error": "no_model_package_arn"}

    item = ddb.get_item(Key={"ModelPackageArn": model_pkg_arn}).get("Item")
    if not item:
        logger.warning("Token not found for %s (maybe SQS not processed yet).", model_pkg_arn)
        return {"warning": "callback_token_not_found"}

    token = item["CallbackToken"]

    # CallbackStep を成功として再開させる（SageMaker API）
    # SendPipelineExecutionStepSuccess を呼ぶ
    try:
        sm.send_pipeline_execution_step_success(
            CallbackToken=token,
            OutputParameters=[{"Name": "Ack", "Value": "approved"}],
        )
        logger.info("Pipeline resumed for %s", model_pkg_arn)
        return {"resumed": True, "ModelPackageArn": model_pkg_arn}
    except ClientError as e:
        logger.exception("Failed to send step success: %s", e)
        raise
