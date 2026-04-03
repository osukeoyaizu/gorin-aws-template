import json
import os
import boto3
resource = boto3.resource('dynamodb')
dynamodb = resource.Table(os.environ['CONNECTION_TABLE'])

def lambda_handler(event, context):
    body = json.loads(event['body'])
    message = body['message']
    sender = body['sender']
    post_data = json.dumps({'message': message, 'sender': sender})
    domain_name = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    items = dynamodb.scan(ProjectionExpression='connection_id').get('Items')
    if items is None:
        return { 'statusCode': 500,'body': 'something went wrong' }
    apigw_management = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url=F"https://{domain_name}/{stage}"
        )
    # 全てのconnection_idに対してデータを送信する
    # IAMポリシー(execute-api:ManageConnections)が必要
    for item in items:
        response = apigw_management.post_to_connection(
            ConnectionId=item['connection_id'],
            Data=post_data
        )
    return { 'statusCode': 200,'body': 'ok' }