## SQS キューまたは SNS トピックが AWS Key Management Service (AWS KMS) カスタマーマネージドキーで暗号化されている場合に必要なキーポリシー

https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html

    {
        "Sid": "example-statement-ID",
        "Effect": "Allow",
        "Principal": {
            "Service": "s3.amazonaws.com"
        },
        "Action": [
            "kms:GenerateDataKey",
            "kms:Decrypt"
        ],
        "Resource": "*"
    }
