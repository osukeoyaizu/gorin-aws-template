import json
import boto3
import os

ssm = boto3.client('ssm')
PARAMETER_NAME = os.environ['PARAMETER_NAME']

# パラメータストアからデータ取得
def get_parameter():
    response = ssm.get_parameter(
        Name=PARAMETER_NAME,
        WithDecryption=True
        )
    return response

def lambda_handler(event, context):
    get_parameter_response = get_parameter()
    parameter = get_parameter_response['Parameter']['Value']

    return {
        'statusCode': 200,
        'body': 'OK'
    }
