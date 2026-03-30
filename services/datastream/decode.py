import json
import base64
import boto3

client = boto3.client('dynamodb')
table_name = 'lab2-table'

def lambda_handler(event, context):
    print((event[0]['data']))
    print(base64.b64decode(event[0]['data']))
    # ただの文字列なのでキーを指定することができない
    data = base64.b64decode(event[0]['data']).decode('utf-8')
    print(data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
