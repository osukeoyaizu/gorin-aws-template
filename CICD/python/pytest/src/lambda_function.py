import json

def lambda_handler(event, context):
    # aaa
    return {
        'statusCode': 200,
        'body': json.dumps({"message":"hello"})
    }

