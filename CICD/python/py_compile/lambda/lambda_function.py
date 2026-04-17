import json

def test():
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

