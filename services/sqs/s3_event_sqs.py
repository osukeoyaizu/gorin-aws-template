import json

def s3_event_sqs(event):
    data = json.loads(event['Records'][0]['body'])
    bucket = data['Records'][0]['s3']['bucket']['name']
    key = data['Records'][0]['s3']['object']['key']
    return bucket, key

def lambda_handler(event, context):
    print(json.dumps(event))

    bucket, key = s3_event_sqs(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }