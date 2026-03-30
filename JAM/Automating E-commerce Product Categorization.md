## task1
### jsonファイル作成
```
{"LambdaFunctionConfigurations": [{"LambdaFunctionArn": "<Lambda関数ARN>", "Events": ["s3:ObjectCreated:Put"]}]}
```
### イベント通知設定
```
aws s3api put-bucket-notification-configuration --bucket "<バケット名>" --notification-configuration file://lambda.json
```
