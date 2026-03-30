https://docs.aws.amazon.com/ja_jp/guardduty/latest/ug/guardduty_exportfindings.html

## KMSキーポリシー
```
{    
    "Sid": "AllowGuardDutyKey",
    "Effect": "Allow",
    "Principal": {
        "Service": "guardduty.amazonaws.com"
    },
    "Action": "kms:GenerateDataKey",
    "Resource": "<KMS key ARN>",
    "Condition": {
        "StringEquals": {
            "aws:SourceAccount": "<account-id>",
            "aws:SourceArn": "arn:aws:guardduty:<region>:<account-id>:detector/<SourceDetectorID>"	
        }
    }
}
```

**KMS key Arn** : CloudFrontのディストリビューションArn

**account-id** : アカウントID

**region** : DuradDutyのリージョン

**SourceDetectorID** : GuardDutuyのディテクターID(設定セクションから確認する)


## S3バケットポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Allow GetBucketLocation",
            "Effect": "Allow",
            "Principal": {
                "Service": "guardduty.amazonaws.com"
            },
            "Action": "s3:GetBucketLocation",
            "Resource": "<S3 bucket Arn>",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "<account-id>",
                    "aws:SourceArn": "arn:aws:guardduty:<region>:<account-id>:detector/<SourceDetectorID>"	

                }
            }
        },
        {
            "Sid": "Allow PutObject",
            "Effect": "Allow",
            "Principal": {
                "Service": "guardduty.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "<S3 bucket Arn>/*",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "<account-id>",
                    "aws:SourceArn": "arn:aws:guardduty:<region>:<account-id>:detector/<SourceDetectorID>"	

                }
            }
        },
        {
            "Sid": "Deny unencrypted object uploads",
            "Effect": "Deny",
            "Principal": {
                "Service": "guardduty.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "<S3 bucket Arn>/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": "aws:kms"
                }
            }
        },
        {
            "Sid": "Deny incorrect encryption header",
            "Effect": "Deny",
            "Principal": {
                "Service": "guardduty.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "<S3 bucket Arn>/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption-aws-kms-key-id": "<KMS key ARN>"
                }
            }
        },
        {
            "Sid": "Deny non-HTTPS access",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "<S3 bucket Arn>/*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
    ]
}
```

**S3 bucket Arn** : S3バケットのArn

**KMS key Arn** : CloudFrontのディストリビューションArn

**account-id** : アカウントID

**region** : DuradDutyのリージョン

**SourceDetectorID** : GuardDutuyのディテクターID(設定セクションから確認する)
