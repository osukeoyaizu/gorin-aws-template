## task1
### S3ゲートウェイエンドポイント作成

名前:My-Vpc-Endpoint

サービス:s3(ゲートウェイ)

VPC:My-Vpc

ルートテーブル:My-Route-Table


## task2
### s3のバケットポリシーを編集する
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::my-s3-bucket-{account-id}/*",
            "Condition": {
                "StringNotEquals": {
                    "aws:SourceVpce": "{s3のVPCエンドポイントID}"
                }
            }
        }
    ]
}
```


## task3
EC2の接続から「パブリックIPを使用して接続」で接続する
```
touch my-test-upload-file
aws s3 cp my-test-upload-file s3://my-s3-bucket-{account-id}
```
