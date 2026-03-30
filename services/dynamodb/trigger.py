import json

PARTITION_KEY = 'id'

def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        print(record)
        eventName = record['eventName']
        approximateCreationDateTime = record['dynamodb']['ApproximateCreationDateTime']
        if eventName == 'INSERT' or eventName == 'MODIFY':
            new_id = record['dynamodb']['NewImage'][PARTITION_KEY]['S']
            # # 列名よって違う
            # new_number = record['dynamodb']['NewImage']['number']['N']
        
        elif eventName == 'REMOVE':
            old_id = record['dynamodb']['Keys'][PARTITION_KEY]['S']
            # # 列名よって違う
            # old_number = record['dynamodb']['OldImage']['number']['N']
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
