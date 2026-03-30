# lambda_deploy_endpoint.py
import os
import json
import boto3
from datetime import datetime, timezone

sagemaker = boto3.client("sagemaker")
sts = boto3.client("sts")

def _region():
    session = boto3.session.Session()
    return session.region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")

def lambda_handler(event, context):
    """
    期待する event（Lambda① から同期呼び出し）:
    {
        "status": "OK",
        "exec_id": "...",
        "training_job_name": "mlops-<ModelName>-<exec_id>",
        "model_data_url": "s3://.../model.tar.gz",  # ← これをそのまま使う
        ...
    }
    """
    # ===== デフォルト付き環境変数 =====
    MODEL_NAME = os.environ.get("MODEL_NAME", "abalone-xgb")

    IMAGE_REPO_NAME = os.environ.get("IMAGE_REPO_NAME", "inference")
    IMAGE_TAG_NAME  = os.environ.get("IMAGE_TAG_NAME", "latest")

    account_id = sts.get_caller_identity()["Account"]
    region = _region()

    EXEC_ROLE_ARN = os.environ.get("EXEC_ROLE_ARN", f"arn:aws:iam::{account_id}:role/MLOps")
    EP_INSTANCE_TYPE  = os.environ.get("ENDPOINT_INSTANCE_TYPE", "ml.m5.large")
    EP_INSTANCE_COUNT = int(os.environ.get("ENDPOINT_INSTANCE_COUNT", "1"))
    ENDPOINT_NAME_PREFIX = os.environ.get("ENDPOINT_NAME_PREFIX", f"{MODEL_NAME}-dev-endpoint")

    # ===== Lambda① からの値 =====
    exec_id = event["exec_id"]
    training_job_name = event["training_job_name"]
    model_data_url = event["model_data_url"]  # ①の DescribeTrainingJob 由来

    # ===== 推論イメージ URI（ECR）=====
    image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{IMAGE_REPO_NAME}:{IMAGE_TAG_NAME}"

    # 1) モデル
    sm_model_name = f"mlops-{MODEL_NAME}-{exec_id}"
    sagemaker.create_model(
        ModelName=sm_model_name,
        PrimaryContainer={
            "Image": image_uri,
            "ModelDataUrl": model_data_url
        },
        ExecutionRoleArn=EXEC_ROLE_ARN
    )

    # 2) EndpointConfig
    epc_name = f"{sm_model_name}-cfg"
    sagemaker.create_endpoint_config(
        EndpointConfigName=epc_name,
        ProductionVariants=[{
            "VariantName": "AllTraffic",
            "ModelName": sm_model_name,
            "InitialInstanceCount": EP_INSTANCE_COUNT,
            "InstanceType": EP_INSTANCE_TYPE,
            "InitialVariantWeight": 1.0
        }]
    )

    # 3) Endpoint
    endpoint_name = ENDPOINT_NAME_PREFIX
    sagemaker.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=epc_name
    )
    # InService まで待つ場合は以下を有効化（Lambda タイムアウトに注意）
    # waiter = sagemaker.get_waiter("endpoint_in_service")
    # waiter.wait(EndpointName=endpoint_name)

    return {
        "status": "OK",
        "endpoint_name": endpoint_name,
        "endpoint_config": epc_name,
        "model_name": sm_model_name,
        "image_uri": image_uri,
        "model_data_url": model_data_url
    }