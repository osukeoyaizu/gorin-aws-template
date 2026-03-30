import json
import os
import logging
import boto3

TABLE = os.environ['CONNECTION_TABLE']
resource = boto3.resource('dynamodb')
dynamodb = resource.Table(TABLE)

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    print(connection_id)
    # connection_idを削除する
    result = dynamodb.delete_item(Key={'connection_id': connection_id})
    return { 'statusCode': 200, 'body': 'ok' }
