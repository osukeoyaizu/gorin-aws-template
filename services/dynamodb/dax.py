import amazondax
import json
import os
from aws_lambda_powertools import Tracer

tracer = Tracer(service="oyaizu-dax")

dax_endpoint_url = os.environ['DAX_ENDPOINT_URL']
dynamodb_table = os.environ['DYNAMODB_TABLE']
region = os.environ['REGION']

dax_client = amazondax.AmazonDaxClient(
    endpoint_url=dax_endpoint_url,
    region_name=region
    )

def query():
    result = dax_client.query(
        TableName=dynamodb_table,
        KeyConditionExpression='id = :id',
        ExpressionAttributeValues={
            ':id': {'N': '1'}
        }
    )
    return result['Items']


def scan():
    result = dax_client.scan(
        TableName=dynamodb_table,
        Limit=100
    )
    return result['Items']


def get_data_byid(id):
    response = dax_client.get_item(
        TableName=dynamodb_table,
        Key={
            'id': {'N': '1'}
        }
    )

    return response['Item']


@tracer.capture_lambda_handler
def lambda_handler(event, context):

    # q_response = query()

    # q_scan = scan()

    get_byid_response = get_data_byid(100)

    return {
        'statusCode': 200,
        'body': json.dumps(get_byid_response, default=str)
    }