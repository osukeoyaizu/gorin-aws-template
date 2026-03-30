import json
import boto3

s3 = boto3.client('s3')

def put_object(bucket, key, body):
    response = s3.put_object(Bucket=bucket, Key=key ,Body=body)
    return response


def lambda_handler(event, context):
    bucket = 'lab2-s3'
    key = 'test/test.txt'
    body = event['body']

    response = put_object(bucket, key, body)
    
    return {
        'statusCode': 200,
        'body': response
    } 