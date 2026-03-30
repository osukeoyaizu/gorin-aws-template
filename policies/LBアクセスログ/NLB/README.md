## S3バケットポリシー
https://docs.aws.amazon.com/ja_jp/elasticloadbalancing/latest/application/enable-access-logging.html
```
{
    "Sid": "AWSLogDeliveryAclCheck",
    "Effect": "Allow",
    "Principal": {
        "Service": "delivery.logs.amazonaws.com"
    },
    "Action": "s3:GetBucketAcl",
    "Resource": "<s3-bucket-arn>",
    "Condition": {
        "StringEquals": {
            "aws:SourceAccount": [
                "<account-id>"
            ]
        },
        "ArnLike": {
            "aws:SourceArn": [
                "arn:aws:logs:<region>:<account-id>:*"
            ]
        }
    }
},
{
    "Sid": "AWSLogDeliveryWrite",
    "Effect": "Allow",
    "Principal": {
        "Service": "delivery.logs.amazonaws.com"
    },
    "Action": "s3:PutObject",
    "Resource": "<s3-bucket-arn>/*",
    "Condition": {
        "StringEquals": {
            "s3:x-amz-acl": "bucket-owner-full-control",
            "aws:SourceAccount": [
                "<account-id>"
            ]
        },
        "ArnLike": {
            "aws:SourceArn": [
                "arn:aws:logs:<region>:<account-id>:*"
            ]
        }
    }
}
```

**s3-bucket-arn**: アクセスログを保存する場所の ARN

**account-id**: リージョンの Elastic Load Balancing AWSアカウントのID

**region**: リージョンコード
