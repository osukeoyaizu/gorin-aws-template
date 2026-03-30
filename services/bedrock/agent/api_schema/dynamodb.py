
import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    action_group = event.get("actionGroup")
    api_path = event.get("apiPath")
    http_method = event.get("httpMethod")
    response_code = 200
    body = {}

    try:
        properties = event.get('requestBody', {}).get('content', {}).get('application/json', {}).get('properties', [])
        table_name = None
        partition_key = None
        sort_key = None

        for element in properties:
            if element.get('name') == 'tableName':
                table_name = element.get('value')
            elif element.get('name') == 'partitionKey':
                partition_key = element.get('value')
            elif element.get('name') == 'sortKey':
                sort_key = element.get('value')

        # --- Create Table ---
        if api_path == '/createTable':
            if not table_name or not partition_key:
                raise ValueError("Missing required parameters: tableName or partitionKey")

            key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}]
            attribute_definitions = [{'AttributeName': partition_key, 'AttributeType': 'S'}]

            if sort_key:
                key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': 'S'})

            response = dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                BillingMode='PAY_PER_REQUEST'
            )

            body = {
                'message': 'Table created successfully',
                'tableArn': response['TableDescription']['TableArn']
            }

        # --- Delete Table ---
        elif api_path == '/deleteTable':
            if not table_name:
                raise ValueError("Missing required parameter: tableName")

            dynamodb.delete_table(TableName=table_name)
            body = {'message': f'Table {table_name} deleted successfully'}

        else:
            response_code = 400
            body = {'error': 'Invalid API path'}

    except Exception as e:
        print(f"Error: {str(e)}")
        response_code = 400
        body = {'error': str(e)}


    # Bedrockエージェント用レスポンス形式
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath": api_path,
            "httpMethod": http_method,
            "httpStatusCode": response_code,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body)
                }
            }
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {})
    }

