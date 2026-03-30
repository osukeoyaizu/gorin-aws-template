import json
import boto3
import os

servicediscovery = boto3.client('servicediscovery')

NAMESPACE_NAME = os.environ['NAMESPACE_NAME']
SERVICE_NAME = os.environ['SERVICE_NAME']

def discover_instances():
    response = servicediscovery.discover_instances(
        NamespaceName=NAMESPACE_NAME,
        ServiceName=SERVICE_NAME,
    )
    return response


def lambda_handler(event, context):
    response = discover_instances()

    return {
        'statusCode': 200,
        'body': json.dumps(response, default=str)
    }
