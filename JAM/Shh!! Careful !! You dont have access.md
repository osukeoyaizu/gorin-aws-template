## task1
s3ゲートウェイエンドポイントを作成する

sagemakerのセキュリティグループのアウトバウンドルールでHTTPSをs3プレフィックスリストに許可する

## task2
### IAMロール(data-science-notebook-role)にインラインポリシー作成
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::ml-model-artifacts-<account-id>-<region>",
                "arn:aws:s3:::ml-model-artifacts-<account-id>-<region>/*"
            ]
        }
    ]
}
```

## task3
### IAMロール(data-science-notebook-role)にインラインポリシー作成
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListBucketAccess",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::ml-training-data-{AccountId}-{AWSRegion}"
        },
        {
            "Sid": "GetObjectAccess",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::ml-training-data-{AccountId}-{AWSRegion}/*"
        }
    ]
}
```

### キーポリシー編集
```
{
    "Sid": "Allow Data Science Notebook Role to use the key",
    "Effect": "Allow",
    "Principal": {
    "AWS": "arn:aws:iam::{ACCOUNT_ID}:role/data-science-notebook-role"
    },
    "Action": [
    "kms:Decrypt"
    ],
    "Resource": "{KMS_KEY_ARN}"
}
```
