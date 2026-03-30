
# lambda_describe_modelpackage_status.py
import boto3

sm = boto3.client("sagemaker")

def lambda_handler(event, context):
    arn = event["ModelPackageArn"]
    resp = sm.describe_model_package(ModelPackageName=arn)
    return {"ApprovalStatus": resp["ModelApprovalStatus"]}
