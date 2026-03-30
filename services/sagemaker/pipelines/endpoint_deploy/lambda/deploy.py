
import json
import time
import boto3
from botocore.exceptions import ClientError

sm = boto3.client("sagemaker")

def _now_suffix():
    # UTCの時刻で一意なサフィックスを作る（例：20260115-041210）
    return time.strftime("%Y%m%d-%H%M%S", time.gmtime())

def _exists(describe_call, **kwargs) -> bool:
    try:
        describe_call(**kwargs)
        return True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("ValidationException", "ResourceNotFound", "ResourceNotFoundException"):
            return False
        raise

def lambda_handler(event, context):
    print(json.dumps(event))
    model_package_arn = event["ModelPackageArn"]
    role_arn           = event["RoleArn"]
    base_model_name    = event.get("ModelName", "abalone-model-from-pkg")
    base_epc_name      = event.get("EndpointConfigName", "abalone-endpoint-config")
    endpoint_name      = event.get("EndpointName", "abalone-endpoint")
    instance_type      = event.get("InstanceType", "ml.m5.xlarge")
    initial_count      = int(event.get("InitialInstanceCount", 1))
    vpc_config         = event.get("VpcConfig")  # 例: {"Subnets": [...], "SecurityGroupIds": [...]}

    # === 1) 一意な命名にする（サフィックス付与）
    suf        = _now_suffix()
    model_name = f"{base_model_name}-{suf}"
    epc_name   = f"{base_epc_name}-{suf}"

    # === 2) CreateModel (ModelPackageをそのまま参照)
    # ここだけ追加：protobuf 互換エラーの回避（純Python実装に強制）
    create_model_kwargs = {
        "ModelName": model_name,
        "PrimaryContainer": {
            "ModelPackageName": model_package_arn,
            "Environment": {
                "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": "python"
            }
        },
        "ExecutionRoleArn": role_arn,
    }
    if vpc_config:
        create_model_kwargs["VpcConfig"] = vpc_config

    sm.create_model(**create_model_kwargs)

    # === 3) CreateEndpointConfig
    sm.create_endpoint_config(
        EndpointConfigName=epc_name,
        ProductionVariants=[{
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": initial_count,
            "InstanceType": instance_type,
            "InitialVariantWeight": 1.0,
        }],
    )

    # === 4) Create or Update Endpoint
    if _exists(sm.describe_endpoint, EndpointName=endpoint_name):
        sm.update_endpoint(EndpointName=endpoint_name, EndpointConfigName=epc_name)
        action = "UpdateEndpoint"
    else:
        sm.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=epc_name)
        action = "CreateEndpoint"

    return {
        "Action": action,
        "EndpointName": endpoint_name,
        "EndpointConfigName": epc_name,
    }