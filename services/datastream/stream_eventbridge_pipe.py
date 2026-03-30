import json
import base64

def lambda_handler(event, context):
    print(json.dumps(event))
    
    for item in event:
        data = base64.b64decode(item['data']).decode('utf-8')
        print(data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }