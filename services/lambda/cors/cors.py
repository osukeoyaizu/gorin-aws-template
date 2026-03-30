import json
import boto3

def lambda_handler(event, context):
    data = []
    for i in range(1,10):
        data.append({'id':i, 'msg':'text%s' % (i)})
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': 'https://xxxxxxxxxx.cloudfront.net', #クライアントがリクエストするURL
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET' #使用されるHTTPメソッド
        },
        'body': json.dumps(data)
    }
