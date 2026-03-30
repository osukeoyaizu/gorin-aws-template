import json

def lambda_handler(event, context):
    commit_id = event['Records'][0]['codecommit']['references'][0]['commit']

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }