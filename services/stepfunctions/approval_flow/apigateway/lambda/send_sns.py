import json
import boto3
import urllib
client = boto3.client('sns')
# APIGatewayのURL
api_url = 'https://pphezyz6ca.execute-api.ap-northeast-1.amazonaws.com/dev'


def lambda_handler(event, context):
    # タスクトークン
    token = event['MyTaskToken']
    #クエリ文字として送信するためにエンコード
    encoded_token = urllib.parse.quote(token)
    # 承認用URL
    approve_url = f"{api_url}/?action=approve&taskToken={encoded_token}"
    # 拒否用URL
    reject_url = f"{api_url}/?action=reject&taskToken={encoded_token}"
    # SNSトピックに送信するメッセージの内容
    message = f"Approve {approve_url}\nReject {reject_url}"
    print(encoded_token)
    
    # SNSトピックにパブリッシュ
    response = client.publish(
        TopicArn='arn:aws:sns:ap-northeast-1:608728620263:lab2-sns',
        Message=message
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
}