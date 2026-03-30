import json
import boto3

s3 = boto3.client('s3')

# オブジェクトをコピー
def copy_object(target_bucket, target_key, source_bucket, source_key):
    s3.copy_object(Bucket=target_bucket, Key=target_key, CopySource={'Bucket': source_bucket, 'Key': source_key})

def lambda_handler(event, context):
    target_bucket = 'target-bucket'
    target_key = 'sample/target.txt'
    source_bucket = 'source-bucket'
    source_key = 'sample/source.txt'
    # オブジェクトをコピー
    copy_object(target_bucket, target_key, source_bucket, source_key)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    } 