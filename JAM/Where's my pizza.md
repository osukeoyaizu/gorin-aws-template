## task1
snsトピックを作成し、パラメータストアにarnを保存する

## task2
### DynamoDBテーブル作成
名前:pizza-orders

パーティションキー:orderId

ソートキー:pizzaName

## task3
### Lambda関数作成
名前:save-pizza-order-to-dynamodb

ランタイム:Python 3.13

実行ロール:OrderedPizzaLambdaRole 

```
import json
import boto3

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('pizza-orders')

def lambda_handler(event, context):
    records = event['Records']
    for item in records:
        message = item['Sns']['Message']

        table.put_item(Item=json.loads(message))
        
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

### SNSでLambdaのサブスクリプションを作成する
task1で作成したsnsトピックのでtask3で作成したLambdaのサブスクリプションを作成する


