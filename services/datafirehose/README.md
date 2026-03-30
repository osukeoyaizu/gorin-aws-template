## パーティショニング
### 取得データ

{"timestamp": "2025-05-22T15:36:17.744018", "source_ip": "10.0.1.55", "path": "/health", "method": "GET", "status": 200, "duration": "0.000087", "partition": 1747932620}


### 動的パーティショニング

#### 文字列データを使用する場合
| キー | 値 |
| ---- | ---- |
| year | .timestamp &#124; gsub("\\\\.\\\\d+$"; "") &#124; strptime("%Y-%m-%dT%H:%M:%S") &#124; strftime("%Y") |
| month | .timestamp &#124; gsub("\\\\.\\\\d+$"; "") &#124; strptime("%Y-%m-%dT%H:%M:%S") &#124; strftime("%m") |
| day | .timestamp &#124; gsub("\\\\.\\\\d+$"; "") &#124; strptime("%Y-%m-%dT%H:%M:%S") &#124; strftime("%d") |
| hour | .timestamp &#124; gsub("\\\\.\\\\d+$"; "") &#124; strptime("%Y-%m-%dT%H:%M:%S") &#124; strftime("%H") |

※timestampがnullの場合のエラー防止
```
if (.timestamp != null and .timestamp != "") then .timestamp | gsub("\\\\.\\\\d+$"; "") | strptime("%Y-%m-%dT%H:%M:%S") | strftime("%Y") else "None" end
```

#### int型の値を使用する場合(例:1747932620)
| キー | 値 |
| ---- | ---- |
| year | .partition &#124;  strftime("%Y") |
| month | .partition &#124; strftime("%m") |
| day | .partition &#124; strftime("%d") |
| hour | .partition &#124; strftime("%H") |

#### バケットプレフィックス
```
firehose/year=!{partitionKeyFromQuery:year}/month=!{partitionKeyFromQuery:month}/day=!{partitionKeyFromQuery:day}/hour=!{partitionKeyFromQuery:hour}/
```

### バケットプレフィックスで設定
```
firehose/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/
```

## 送信先でHTTPエンドポイントを指定
### DataFirehoseの設定
送信先:HTTPエンドポイント

HTTPエンドポイントURL:https://xxxxxyyyyy.execute-api.{region}.amazonaws.com/prod



### API Gatewayの設定
メソッド:POST

統合タイプ:Lambda

### Lambda
```
import json
import base64
import datetime

def lambda_handler(event, context):
    body = json.loads(event['body'])

    for record in body['records']:
        json_data = base64.b64decode(record['data']).decode('utf-8')
        dict_data = json.loads(json_data)
        print(dict_data)

    # firehoseへ適切な形式のレスポンス
    requestId = body['requestId']
    response = {
            "requestId": requestId,
            "timestamp": datetime.datetime.now().timestamp()
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
```

### APIキーを使用する場合
APIキーと使用量プランを作成してステージに関連付ける

#### Lambda関数(オーソライザ用)
```
import json
import os

def lambda_handler(event, context):
    print(json.dumps(event))
    # ヘッダーからキーを取得
    headers = event.get("headers", {})
    firehose_key = headers.get("X-Amz-Firehose-Access-Key")

    expected_key = os.environ.get("EXPECTED_FIREHOSE_KEY")

    effect = 'Deny'

    if firehose_key == expected_key:
        effect = 'Allow'

    print(effect)

    return {
        'principalId': '*',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': event['methodArn']
                }
            ]
        }
    }

```

#### Lambdaオーソライザ
Lambdaイベントペイロード:リクエスト

ヘッダー:X-Amz-Firehose-Access-Key

※POSTメソッドの認可設定で選択する

#### Firehoseの設定

アクセスキー:{apiキーの値}

