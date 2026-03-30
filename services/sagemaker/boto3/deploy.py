
# -*- coding: utf-8 -*-
import json
import os
import time
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ===== 環境変数 =====
MODEL_NAME_PREFIX = os.environ.get("MODEL_NAME_PREFIX", "my-model")
ENDPOINT_CONFIG_PREFIX = os.environ.get("ENDPOINT_CONFIG_PREFIX", "my-endpoint-config")
ENDPOINT_NAME = os.environ.get("ENDPOINT_NAME", "my-endpoint")

INSTANCE_TYPE = os.environ.get("INSTANCE_TYPE", "ml.m5.xlarge")
INITIAL_INSTANCE_COUNT = int(os.environ.get("INITIAL_INSTANCE_COUNT", "1"))

ROLE_ARN = os.environ.get("ROLE_ARN", "arn:aws:iam::xxxxxxyyyyyy:role/service-role/AmazonSageMaker-ExecutionRole-20260116T162201")

VPC_SUBNETS = [
    s.strip()
    for s in os.environ.get("VPC_SUBNETS", "subnet-0e85ff4e06f1ddcde,subnet-037632603c48b11eb,subnet-0e11282bc27136243").split(",")
    if s.strip()
]

VPC_SECURITY_GROUP_IDS = [
    s.strip()
    for s in os.environ.get("VPC_SECURITY_GROUP_IDS", "sg-06aa14a983d3799dd").split(",")
    if s.strip()
]

CONTAINER_ENV_JSON = os.environ.get("CONTAINER_ENV", '{"LOG_LEVEL":"INFO"}')


sm = boto3.client("sagemaker")

# ===== みにくい関数（元のまま） =====

def create_model(model_package_arn, role_arn, model_name, environment=None, vpc_config=None):
    kwargs = {
        "ModelName": model_name,
        "PrimaryContainer": {
            "ModelPackageName": model_package_arn,
            "Environment": environment or {}
        },
        "ExecutionRoleArn": role_arn,
    }
    if vpc_config:
        kwargs["VpcConfig"] = vpc_config

    logger.info("CreateModel: %s", json.dumps(kwargs, default=str))
    return sm.create_model(**kwargs)


def create_endpoint_config(endpoint_config_name, model_name, instance_type, initial_count):
    kwargs = {
        "EndpointConfigName": endpoint_config_name,
        "ProductionVariants": [{
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": initial_count,
            "InstanceType": instance_type,
            "InitialVariantWeight": 1.0
        }]
    }
    logger.info("CreateEndpointConfig: %s", json.dumps(kwargs, default=str))
    return sm.create_endpoint_config(**kwargs)


def update_endpoint(endpoint_name, endpoint_config_name):
    logger.info("UpdateEndpoint → %s", endpoint_config_name)
    return sm.update_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name
    )


def create_endpoint(endpoint_name, endpoint_config_name):
    logger.info("CreateEndpoint → %s", endpoint_name)
    return sm.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name
    )


# ===== Lambda Handler（短くて読みやすい版）=====
def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event, default=str))
    print(VPC_SECURITY_GROUP_IDS)

    # --- 必須パラメータ ---
    # model_package_arn = event["ModelPackageArn"]
    model_package_arn = "arn:aws:sagemaker:us-east-1:140083316867:model-package/abalone-model-new-sdk/2"

    # --- 一意な名前 ---
    suffix = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    model_name = f"{MODEL_NAME_PREFIX}-{suffix}"
    epc_name = f"{ENDPOINT_CONFIG_PREFIX}-{suffix}"

    # --- VPC Config（存在すれば適用） ---
    vpc_config = None
    if VPC_SUBNETS or VPC_SECURITY_GROUP_IDS:
        vpc_config = {
            "Subnets": VPC_SUBNETS,
            "SecurityGroupIds": VPC_SECURITY_GROUP_IDS,
        }

    # --- コンテナ環境変数 ---
    container_env = {
        "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": "python"
    }
    if CONTAINER_ENV_JSON:
        container_env.update(json.loads(CONTAINER_ENV_JSON))

    # --- Create Model & EndpointConfig ---
    create_model(
        model_package_arn=model_package_arn,
        role_arn=ROLE_ARN,
        model_name=model_name,
        environment=container_env,
        vpc_config=vpc_config
    )

    create_endpoint_config(
        endpoint_config_name=epc_name,
        model_name=model_name,
        instance_type=INSTANCE_TYPE,
        initial_count=INITIAL_INSTANCE_COUNT
    )

    # --- エンドポイントが存在するかチェック ---
    try:
        sm.describe_endpoint(EndpointName=ENDPOINT_NAME)
        action = "UpdateEndpoint"
    except ClientError:
        action = "CreateEndpoint"

    # --- Create or Update ---
    if action == "UpdateEndpoint":
        update_endpoint(ENDPOINT_NAME, epc_name)
    else:
        create_endpoint(ENDPOINT_NAME, epc_name)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "action": action,
            "endpointName": ENDPOINT_NAME,
            "endpointConfigName": epc_name,
            "modelName": model_name,
            "instanceType": INSTANCE_TYPE,
            "initialInstanceCount": INITIAL_INSTANCE_COUNT,
            "vpcUsed": bool(vpc_config)
        }, ensure_ascii=False)
    }
