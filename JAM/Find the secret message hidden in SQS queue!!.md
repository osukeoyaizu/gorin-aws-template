## task1
### SQS用VPCエンドポイントのセキュリティグループにインバウンドルール追加
タイプ:HTTPS

ソース:Lambdaのセキュリティグループ(lambda-sg)

## task2
### IAMロール(Jam-Challenge-Role)のIAMポリシー(LambdaSQSAccess)に以下のステートメントを追加する
```
{
    "Sid": "Statement1",
    "Effect": "Allow",
    "Action": [
        "sqs:GetQueueUrl",
        "sqs:ReceiveMessage",
        "sqs:SendMessage"
    ],
    "Resource": ["<sqs-arn>"]
}
```

Lambda関数をテストする
