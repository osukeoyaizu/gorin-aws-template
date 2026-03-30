import boto3
import json

s3 = boto3.client('s3')

def get_object(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response


def lambda_handler(event, context):
    bucket = 'my-s3-bucket'
    key = 'test_transcription.json'
    get_object_response = get_object(bucket, key)
    
    # ファイルの内容を読む
    body = get_object_response['Body'].read()
    decoded_body = json.loads(body.decode())
    text = decoded_body['results']['transcripts'][0]['transcript']
    print(text)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }