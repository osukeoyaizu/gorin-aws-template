## task1
### ログ、レプリケーション用のs3バケットを作成する
バケット名:my-jam-logging-bucket-{account-id}

### s3(7-gems-s3-bucket)の設定を変更する
1.パブリックアクセスをすべてブロック

2.バージョニング有効化

3.アクセスログの有効化

4.レプリケーションルールの作成(myS3ReplRoleのIAMロール使用)

5.バケットポリシー編集
```
{
    "Id": "ExamplePolicy",
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSSLRequestsOnly",
            "Action": "s3:*",
            "Effect": "Deny",
            "Resource": [
                "arn:aws:s3:::{bucket-name}",
                "arn:aws:s3:::{bucket-name}/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            },
            "Principal": "*"
        }
    ]
}
```

6.デフォルトの暗号化設定をSSE-KMSに変更する

### Configの適合パックをデプロイする
サンプルテンプレート:Operational Best Practices for Amazon S3

名前:任意

