import json
import boto3

s3 = boto3.client('s3')

# s3バケットからファイルを取得する
def get_object(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response

def lambda_handler(event, context):
    bucket = 'lab2-s3'
    key = 'test/test.txt'
    # s3バケットからファイルを取得する
    s3_object = get_object(bucket, key)
  
    # ファイルの内容を読む
    body = s3_object['Body'].read()
    decoded_body = body.decode()
    print(decoded_body)

    return {
        'statusCode': 200,
        'body': s3_object
    } 