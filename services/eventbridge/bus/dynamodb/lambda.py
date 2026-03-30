import json

PARTITION_KEY = 'id'

def lambda_handler(event, context):
    detail = event['detail']
    eventName = detail['eventName']
    approximateCreationDateTime = detail['dynamodb']['ApproximateCreationDateTime']
    if eventName == 'INSERT' or eventName == 'MODIFY':
        new_id = detail['dynamodb']['NewImage'][PARTITION_KEY]['S']
        # # 列名よって違う
        # new_number = detail['dynamodb']['NewImage']['name']['S']
    elif eventName == 'REMOVE':
        old_id = detail['dynamodb']['Keys'][PARTITION_KEY]['S']
        # # 列名よって違う
        # old_number = detail['dynamodb']['OldImage']['name']['S']

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
