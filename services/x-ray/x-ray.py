import json
import boto3
import os
from aws_xray_sdk.core import patch_all

patch_all()

table = os.environ['TABLE']
region = os.environ['REGION']
dynamodb = boto3.client('dynamodb', region_name=region)

def lambda_handler(event, context):
    
    response = dynamodb.scan(TableName=table)
	    
	    
    return {
        'statusCode': 200,
        'body': response['Items']
    }



#レイヤーインストール方法
# mkdir python
# cd python
# pip install aws-xray-sdk -t .
# zip -r xray.zip ../python/