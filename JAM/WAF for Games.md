## task1
### s3バケットポリシー編集
```
{
    "Version": "2008-10-17",
    "Id": "Basic S3 Bucket Policy",
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{account-id}:root"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{bucket-name}/*"
        }
    ]
}
```

## task2
CloudFrontでOAIを作成する

### s3バケットポリシー編集(task1のポリシーを上書き)
```
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {OAIのID}"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{bucket-name}/*"
        }
    ]
}
```

## task3
WAFのルールからクエリパラメータを確認する

https://xxxxxyyyy.cloudfront.net/secret.html?{クエリパラメータ}=passcode
