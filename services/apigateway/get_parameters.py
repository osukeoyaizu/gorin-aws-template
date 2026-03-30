import json

def lambda_handler(event, context):
    # HTTPメソッド
    httpMethod = event['httpMethod']

    # ヘッダー
    headers = event['headers']

    # クエリ文字列
    queryStringParameters = event['queryStringParameters']

    # パスパラメータ
    pathParameters = event['pathParameters']

    # ボディ
    body = event['body']

    print(httpMethod)
        # PUT
    print(headers)
        # {
        #     'accept': '*/*',
        #     'content-type': 'application/x-www-form-urlencoded',
        #     'header1': 'value1',
        #     'header2': 'value2',
        #     'Host': '○○○○○○.execute-api.ap-northeast-1.amazonaws.com',
        #     'User-Agent': 'curl/8.5.0',
        #     'X-Amzn-Trace-Id': 'Root=1-67e34d8b-16cbed6d048dcc227ba93dff',
        #     'X-Forwarded-For': '57.181.40.77',
        #     'X-Forwarded-Port': '443',
        #     'X-Forwarded-Proto': 'https'
        # }
    print(queryStringParameters)
        # {'param1': '1', 'param2': '2'}
    print(pathParameters)
        # {'id': '123'}
    print(body)
        # {
        #     "id": 1,
        #     "name": "oyaizu"
        # }

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



#リクエスト内容
# curl -X PUT -H 'header1:value1' -H 'header2:value2' -d '{"id": 1, "name": "oyaizu"}' 'https://○○○○○○.execute-api.ap-northeast-1.amazonaws.com/default/123?param1=1&param2=2'