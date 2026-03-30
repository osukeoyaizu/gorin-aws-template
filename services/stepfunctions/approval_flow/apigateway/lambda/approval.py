import json
import boto3
import urllib
client = boto3.client('stepfunctions')
def lambda_handler(event, context):
    # クエリ文字取得
    queryStringParameters = event['queryStringParameters']
    action = queryStringParameters['action']
    token = queryStringParameters['taskToken']
    # tokenをデコードする
    decoded_token = urllib.parse.unquote(token)
    
    # approveの処理
    if action == 'approve':
        client.send_task_success(
            taskToken=decoded_token,
            output=json.dumps({
                "result": action
            })
        )
    # rejectの処理
    elif action == 'reject':
        client.send_task_success(
            taskToken=decoded_token,
            output=json.dumps({
                "result": action
            })
        )
    # 例外の場合は処理を失敗させる
    else:
        client.send_task_failure(
            taskToken=token,
            error=json.dumps({
                "result": action
            })
        )
    return {
        'statusCode': 200,
        'body': action
    }
