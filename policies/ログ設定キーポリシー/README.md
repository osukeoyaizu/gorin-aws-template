## AWSサービスがKMSキーを使って暗号化・復号化するためのポリシー

```
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "fargate.amazonaws.com",
          "logging.s3.amazonaws.com",
          "logs.amazonaws.com",
          "delivery.logs.amazonaws.com",
          "cloudwatch.amazonaws.com",
          "lambda.amazonaws.com",
          "cloudtrail.amazonaws.com",
          "events.amazonaws.com",
          "emr-serverless.amazonaws.com"
        ]
      },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey",
        "kms:CreateGrant"
      ],
      "Resource": "*"
    }
```