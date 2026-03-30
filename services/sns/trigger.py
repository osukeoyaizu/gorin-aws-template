import json

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    print(message)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }