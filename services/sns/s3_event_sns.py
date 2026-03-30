import json

def s3_event_sqs(event):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    bucket = sns_message['Records'][0]['s3']['bucket']['name']
    key = sns_message['Records'][0]['s3']['object']['key']
    return bucket, key


def lambda_handler(event, context):
    bucket, key = s3_event_sqs(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }