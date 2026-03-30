import os
import boto3
import json
from botocore.client import Config

s3 = boto3.client('s3', config=Config(signature_version='s3v4', s3={'addressing_style': 'virtual'}))


def generate_presigned_url(bucket, key, expiration_time, clientMethod, httpMethod):
    signed_url = s3.generate_presigned_url(
        ClientMethod = clientMethod,
        Params = {'Bucket' : bucket, 'Key' : key},
        ExpiresIn = expiration_time,
        HttpMethod = httpMethod
        )
    return signed_url

def lambda_handler(event, context):
    bucket = 'my-bucket'
    key = 'my-key'
    expiration_time = 3600

    # GET用
    get_url = generate_presigned_url(bucket, key, expiration_time, 'get_object', 'GET')

    # PUT用
    put_url = generate_presigned_url(bucket, key, expiration_time, 'put_object', 'PUT')

    return {
        'statusCode': 200,
        'body': json.dumps({'signedUrl': put_url})
    }




# 確認方法
# curl -X PUT --upload-file <ローカルのファイル> '<署名付きURL>' 