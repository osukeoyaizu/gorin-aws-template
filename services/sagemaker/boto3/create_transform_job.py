import json
import boto3
import os
import datetime

s3 = boto3.client("s3")
sagemaker = boto3.client("sagemaker")

def lambda_handler(event, context):
    MODEL_NAME = os.environ["MODEL_NAME"]

    INPUT_BUCKET = os.environ["INPUT_BUCKET"]
    INPUT_PREFIX = os.environ["INPUT_PREFIX"]

    input_path = f"s3://{INPUT_BUCKET}/{INPUT_PREFIX}"

    dt_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # suffix for output path to ensure unique output location for each job
    OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "s3://inference-result/result") + f"/{dt_str}"
    INSTANCE_TYPE = os.environ.get("INSTANCE_TYPE", "ml.m5.large")
    INSTANCE_COUNT = int(os.environ.get("INSTANCE_COUNT", "1"))

    job_name = f"{MODEL_NAME}-{dt_str}"

    try:
        # SageMakerバッチ変換ジョブの呼び出し
        response = sagemaker.create_transform_job(
            TransformJobName=job_name,
            ModelName=MODEL_NAME,
            TransformInput={
                "DataSource": {
                    "S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": input_path}
                },
                "ContentType": "text/csv",
                "SplitType": "Line",
            },
            TransformOutput={
                "S3OutputPath": OUTPUT_PATH,
                "AssembleWith": "Line",
                "Accept": "text/csv",
            },
            TransformResources={
                "InstanceType": INSTANCE_TYPE,
                "InstanceCount": INSTANCE_COUNT,
            },
            DataProcessing={"OutputFilter": "$"},
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"job_name": job_name, "job_arn": response["TransformJobArn"]}
            ),
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
