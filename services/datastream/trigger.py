import json
import base64

def lambda_handler(event, context):
    records = event['Records']

    for record in records:
        data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        print(data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

