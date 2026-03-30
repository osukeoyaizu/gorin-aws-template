import json
import requests
import io
import boto3
import base64

s3 = boto3.client('s3')

image_url = 'https://chocottopro.com/wp-content/uploads/2024/04/requests.jpg'

def put_object(bucket, key, body):
    response = s3.put_object(Bucket=bucket, Key=key ,Body=body)

    return response


def lambda_handler(event, context):
    # URLから画像データ取得
    requests_response = requests.get(image_url)

    # 取得したバイナリデータをファイルオブジェクトに変換
    img = io.BytesIO(requests_response.content)

    bucket = 'sample-s3-bucket'
    key = 'images/test.jpeg'
    body = img
    put_object(bucket, key, body)

    
    # # リクエストボディからデータを取得
    # base64_data = event['body']

    # # デコードして画像データに戻す
    # decoded_data = base64.b64decode(base64_data)
    
    # bucket = 'lab2-s3'
    # key = 'images/' + str(uuid.uuid4()) + '.jpg'
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
