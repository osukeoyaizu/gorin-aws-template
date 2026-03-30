import json
import requests
import io
import pandas as pd

url = 'https://xxxxxxxxxx.cloudfront.net/test.csv'

def lambda_handler(event, context):
    res = requests.get(url)

    # レスポンスボディをテキスト形式で取得
    print(res.text)

    df = pd.read_csv(io.StringIO(res.text))
    print(df)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
