## ステージ変数を使用してLambdaエイリアスを呼び出す
### Lambda関数エイリアス作成
prod:バージョン1

dev:LATEST

### メソッド作成でLambda関数指定
LambdaARN:${stageVariables.alias}

**許可追加のAWS CLIコマンドをステージ分実行する**

**※aliasはステージ変数名と合わせる**

### API Gatewayでステージ変数設定
#### devステージ
名前:{ステージ変数名}

値:dev

#### prodステージ
名前:{ステージ変数名}

値:prod

## SQSにデータ送信
### 前提条件
API Gateway用のIAMロールを作成し、sqs:SendMessageをアタッチ

### メソッド作成
メソッド:POST

統合タイプ:AWSのサービス

AWSのサービス:SQS

HTTPメソッド:POST

パスオーバーライドを使用

パスオーバーライド:{account-id}/oyaizu-test-sqs

実行ロール:{作成したもの}

### 統合リクエストを編集
コンテンツの処理:パススルー

リクエスト本文のパススルー:不可

#### URLリクエストヘッダーのパラメータ
名前:Content-Type
マッピング元:'application/x-www-form-urlencoded'

#### マッピングテンプレート
コンテンツタイプ:application/json

テンプレート本文(標準キュー)
```
Action=SendMessage&MessageBody=$input.body&MessageAttribute.1.Name=HttpMethod&MessageAttribute.1.Value.StringValue=$context.httpMethod&MessageAttribute.1.Value.DataType=String
```
テンプレート本文(FIFOキュー)
①リクエストボディにMessageGroupIdとMessageDeduplicationIdを含める
```
#set($dedupId = $input.json('$.MessageDeduplicationId'))
#set($groupId = $input.json('$.MessageGroupId'))
Action=SendMessage&MessageBody=$util.urlEncode($input.body)&MessageGroupId=$util.urlEncode($groupId)&MessageDeduplicationId=$util.urlEncode($dedupId)
```
②クエリ文字列にMessageGroupIdを含める
```
#set($dedupId = $context.requestId)
Action=SendMessage&MessageBody=$input.body&MessageGroupId=$input.params('MessageGroupId')&MessageDeduplicationId=$dedupId
``` 

## StepFunctionsを非同期呼び出し
### 前提条件
API Gateway用のIAMロールを作成し、states:StartSyncExecutionをアタッチ

### メソッド作成
メソッド:POST

統合タイプ:AWSのサービス

AWSのサービス:Step Functions

HTTPメソッド:POST
   
アクション名を使用

アクション名:StartSyncExecution

実行ロール:{作成したもの}

### 統合リクエストを編集
#### マッピングテンプレート
コンテンツタイプ:application/json

テンプレート本文(統合リクエスト)
```
#set($input = $input.json('$'))
{
"input": "$util.escapeJavaScript($input)",
"stateMachineArn": "arn:aws:states:ap-northeast-1:XXXXXXXXXXX:stateMachine:ステートマシン名"
}
```
テンプレート本文(統合レスポンス)
```
#set ($parsedPayload = $util.parseJson($input.json('$.output')))
$parsedPayload
```


## Firehoseにデータ送信
メソッド:POST

統合タイプ:AWSのサービス

AWSのサービス:Firehose

HTTPメソッド:POST
   
アクション名を使用

アクション名:PutRecord

実行ロール:{作成したもの}

### 統合リクエストを編集
#### マッピングテンプレート
コンテンツタイプ:application/json

テンプレート本文(統合リクエスト)
```
{
    "DeliveryStreamName": "{STREAM_NAME}",
    "Record": {
     "Data": "$util.base64Encode($input.json('$'))"
    }
}
```
