## task1
Lambda関数(individualFinder)を編集
```
import boto3
import json
import os

def handler(event, context):

    bucket_name = os.environ['bucketName']
    filename='locationString.txt'
    s3 = boto3.resource('s3')

    # Insert Code here 
    # Read s3 bucket object and assign the content to the body variable
    body = s3.Object(bucket_name, filename).get()['Body'].read().decode('utf-8')

    resp = {
        "statusCode" : 200,
        "body" : "{\"secret\": \"" + body + "\"}"
    }

    return resp  
```

## task2
Lambdaのコンソール画面からトリガーでAPIGatewayを作成し、URLへアクセスして回答を取得する
