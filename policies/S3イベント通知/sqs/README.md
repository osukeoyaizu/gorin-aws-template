## 発行先SQSキューのIAMポリシー(キューポリシー)
https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html

        {
            "Version": "2012-10-17",
            "Id": "example-ID",
                "Statement": [
                    {
                        "Sid": "example-statement-ID",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "s3.amazonaws.com"
                        },
                        "Action": [
                            "SQS:SendMessage"
                        ],
                        "Resource": "<sqs-queue-Arn>",
                        "Condition": {
                            "ArnLike": {
                                "aws:SourceArn": "<s3-bucket-Arn>"
                            },
                            "StringEquals": {
                                "aws:SourceAccount": "<bucket-owner-account-id>"
                            }
                        }
                }
        ]
        }

**sqs-queue-Arn** : SQSキューのArn

**s3-bucket-Arn** : イベント通知を設定するs3のArn

**bucket-owner-account-id** : s3バケットの所有者のアカウントID
