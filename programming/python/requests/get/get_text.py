import json
import requests

url = 'https://1w7awxfru1.execute-api.ap-northeast-1.amazonaws.com/dev'

def lambda_handler(event, context):
    res = requests.get(url)

    # ステータスコード
    print(res.status_code)

    # レスポンスボディをテキスト形式で取得
    print(res.text)

    # レスポンスボディをバイナリ形式で取得
    print(res.content)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
