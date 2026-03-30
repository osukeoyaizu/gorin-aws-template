## CloudFront OAC による SSE-KMS の KMS キーへのアクセスを許可する KMS キーポリシーステートメント
https://docs.aws.amazon.com/ja_jp/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

    {
        "Sid": "AllowCloudFrontServicePrincipalSSE-KMS",
        "Effect": "Allow",
        "Principal": {
            "Service": [
                "cloudfront.amazonaws.com"
            ]
         },
        "Action": [
            "kms:Decrypt",
            "kms:Encrypt",
            "kms:GenerateDataKey*"
        ],
        "Resource": "*",
        "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "<CloudFront distribution Arn>"
                }
            }
    }

**CloudFront distribution Arn** : CloudFrontのディストリビューションArn


## OAIを使用する際のバケットポリシー
```
{
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity <origin access identity ID>"
    },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::<bucket-name>/*"
}
```