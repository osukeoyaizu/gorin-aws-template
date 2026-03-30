
import boto3
import os

TABLE = os.environ['TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE)

# 専用関数: DynamoDBでユーザー名を検索
def query_user_by_key(key, value):
    if key not in ["email", "phone"]:
        return f"Invalid key: {key}. Must be 'email' or 'phone'."
    
    try:
        index_name = f"{key}-index"  # email-index or phone-index
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=f"{key} = :val",
            ExpressionAttributeValues={":val": value}
        )
        items = response.get("Items", [])
        if items:
            return items[0]["username"]
        else:
            return f"Could not find a user with {key} of {value}"
    except Exception as e:
        return f"Error accessing DynamoDB: {str(e)}"

# Lambdaハンドラー
def lambda_handler(event, context):
    parameters = {p["name"]: p["value"] for p in event.get("parameters", [])}
    key = parameters.get("key")
    value = parameters.get("value")

    print(key)
    print(value)

    body = query_user_by_key(key, value)

    print(body)

    return {
        "response": {
            "actionGroup": event.get("actionGroup"),
            "function": event.get("function"),
            "functionResponse": {
                "responseBody": {
                    "TEXT": {"body": body}
                }
            }
        },
        "messageVersion": event.get("messageVersion", "1.0")
    }


# dynamodbの構造
# username → ユーザー名（PK, 型: String）
# email → メールアドレス（型: String）
# phone → 電話番号（型: String）

# GSI1: email-index（パーティションキー: email）
# GSI2: phone-index（パーティションキー: phone）