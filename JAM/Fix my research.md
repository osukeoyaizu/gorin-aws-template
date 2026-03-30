## task1
VPCルートテーブルでIGWのルートを削除し、s3のゲートウェイエンドポイントを作成する

## task2
セキュリティグループのアウトバウンドルールを編集する

タイプ:HTTPS

送信先:s3のプレフィックスリスト

## task3
キーポリシーでLambdaのロールを許可する
```
{
      "Sid": "Statement1",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<LambdaのロールARN>"
      },
      "Action": "kms:*",
      "Resource": "*"
    }
```
