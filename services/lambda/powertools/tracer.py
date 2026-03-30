import json
from aws_lambda_powertools import Tracer

tracer = Tracer(service="oyaizu-service")

@tracer.capture_lambda_handler
def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': json.dumps('OK', default=str)
    }