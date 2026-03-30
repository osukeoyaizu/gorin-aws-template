## task1
### サービス、ルート作成
サービス名:任意

サービスエンドポイントタイプ:VPC

VPC:modjam-vpc

エンドポイント:出力プロパティのMonolithendpoint

このサービスをアプリケーションのデフォルトルートとして設定しますにチェックをつける

このデフォルトルートをアクティブ状態で作成

**<サービスID>,<ルートID>を回答する**

## task2
### SNSトピック作成
タイプ:スタンダード

名前:NewPolicyRequests

### Lambda(NewPolicyRequest)コード編集
**※topic-arnを作成したsnsのarnに変更する**
```
import boto3
from botocore.config import Config
import json
import os
import uuid

TABLE_NAME = os.environ['TABLE_NAME']
                        
config = Config(connect_timeout=5, read_timeout=5, retries={'max_attempts': 1})
dynamodb = boto3.client('dynamodb', config=config)
sns = boto3.client('sns', config=config)

def is_invalid(request):
    return False

def lambda_handler(event, context):
    print('EVENT: {}'.format(json.dumps(event)))
    
    body = ('{}'.format(json.dumps(event)))

    request = json.loads(body)
    
    if is_invalid(request):
        return {
            'statusCode': 400,
            'body': json.dumps({})
        }
    
    print('Request is valid!')
          
    id = str(uuid.uuid4())
    request['id'] = id
    
    #Get attributes
    customername = ""
    petname1 = ""
    pettype1 = ""
    petname2 = ""
    pettype2 = ""

    for record in request['Records']:
        customername = record['Sns']['MessageAttributes']['customername']['Value']
        petname1 = record['Sns']['MessageAttributes']['petname1']['Value']
        pettype1 = record['Sns']['MessageAttributes']['pettype1']['Value']
        petname2 = record['Sns']['MessageAttributes']['petname2']['Value']
        pettype2 = record['Sns']['MessageAttributes']['pettype2']['Value']
        
    response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            'id': {'S': id},
            'customername': {'S': customername},
            'petname1': {'S': petname1},
            'pettype1': {'S': pettype1},
            'petname2': {'S': petname2},
            'pettype2': {'S': pettype2}
            }
        )
    response = sns.publish(
     TopicArn='<topic-arn>',
     Message=json.dumps(request),
     MessageAttributes = {
        'customername': {
           'DataType': 'String',
           'StringValue': customername
        },
        'petname1': {
           'DataType': 'String',
           'StringValue': petname1
        },
        'pettype1': {
           'DataType': 'String',
           'StringValue': pettype1
        },
        'petname2': {
           'DataType': 'String',
           'StringValue': petname2
        },
        'pettype2': {
           'DataType': 'String',
           'StringValue': pettype2
        }
   }
   )
    return {
        'statusCode': 201,
        'body': json.dumps({
            "customer": "customername"
        })
    }
          

```

## task3
### Lambda(PetCounter)コード編集
```
import json

# import requests

def lambda_handler(event, context):    

    #number of cats
    numberofpets = 0

#get data from event records
    for record in event['Records']:
        #count number of MessageAttributes in record
        if len(record['Sns']['MessageAttributes']) > 0:
            #get MessageAttributes
            messageAttributes = record['Sns']['MessageAttributes']
            #Count number of pets in messageAttributes
            for key in messageAttributes:
                #if key contains pettype
                if 'pettype' in key:
                    #increment numberofpets
                        numberofpets += 1
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "number of pets " + str(numberofpets),
        }),
    }
```

## task4
snsトピックでLambda(LargeAccountNotification)のサブスクリプションを作成する

課題で指示されたJSONを使用してサブスクリプションフィルターポリシーを設定する


## task4
### サービス、ルート作成
サービス名:任意

サービスエンドポイントタイプ:Lambda

Lambda関数:NewPolicyRequest

ソースパス:/newpolicyrequests

このデフォルトルートをアクティブ状態で作成

**<サービスID>,<ルートID>を回答する**
