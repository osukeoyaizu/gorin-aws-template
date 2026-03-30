import json
import os
import boto3

runtime = boto3.client("sagemaker-runtime")
ENDPOINT_NAME = os.environ["ENDPOINT_NAME"]

def lambda_handler(event, context):
    body = json.loads(event["body"])
    payload = body["payload"]  # 例: "0.5,0.44,0.15,0.08,0.2,0.07,0.09,0.05"

    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="text/csv",
        Body=payload.encode("utf-8")
    )

    result = response["Body"].read().decode("utf-8").strip()

    return {
        "statusCode": 200,
        "body": json.dumps({"score": float(result)})
    }