## CloudFront+ALB 構成のオリジンアクセスをカスタムヘッダーで制限する 
### CloudFrontにカスタムヘッダーを付与
ヘッダー名:X-Custom-Header

値:任意の値

### ALBのリスナールールを設定
条件タイプ:HTTPヘッダー

ヘッダー名:{CloudFrontで設定したものと同じヘッダー名}

値:{CloudFrontで設定したものと同じ値}

## ALBで複数AZに負荷分散
別AZのインスタンスをターゲットグループに追加する

ターゲットグループの維持設定のチェックを外す

## クロスゾーン負荷分散を有効にする
NLB → 属性 → クロスゾーン負荷分散を有効にする



## ライフサイクルフックでインスタンス終了時にnginxのログをS3バケットに保存
### 前提条件
インスタンスのIAMロールにs3:PutObject

LambdaのIAMロールにssm:SendCommand


### Systems Managerドキュメントの作成
ターゲットタイプ:/AWS::EC2::Instance
ドキュメントタイプ:Command
```
{
    "schemaVersion": "2.2",
    "description": "log upload",
    "parameters": {},
    "mainSteps": [
      {
        "action": "aws:runShellScript",
        "name": "configureServer",
        "inputs": {
          "runCommand": [
            "instanceid=(`ec2-metadata -i | cut -d ' ' -f 2`)",
            "aws s3 cp /var/log/nginx/access.log s3://{sample}/$instanceid/"
          ]
        }
      }
    ]
  }
```

### Lambda関数作成
```
import json
import boto3

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    EC2InstanceId = event['detail']['EC2InstanceId']
    
    response = ssm.send_command(
        InstanceIds = [EC2InstanceId],
        DocumentName = 'sample-document'
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

### Eventbridgeルール作成
イベントパターン
```
{
  "source": ["aws.autoscaling"],
  "detail-type": ["EC2 Instance-terminate Lifecycle Action"]
}
```
ターゲット:Lmabda関数

### Auto Scaling Groupでライフサイクルフック作成
ライフスタイル移行:インスタンス終了

ハートビートタイムアウト:3600

デフォルトの結果:CONTINUE


