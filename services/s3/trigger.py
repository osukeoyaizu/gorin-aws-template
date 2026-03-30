import json
import boto3

def s3_trigger(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    return bucket, key


def lambda_handler(event, context):

    bucket, key = s3_trigger(event)

    return {
        'statusCode': 200,
        'body': 'OK'
    } 