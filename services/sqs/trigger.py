import json

def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        message = record['body']
        print(message)
        
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }