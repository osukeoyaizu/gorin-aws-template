## Lambda関数でSQSキューをトリガーにする際に必要なポリシー

https://docs.aws.amazon.com/ja_jp/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-lambda-function-trigger.html

        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "sqs:DeleteMessage",
                        "sqs:ReceiveMessage",
                        "sqs:GetQueueAttributes"
                    ],
                    "Resource": "<target-account-queue-arn>"
                }
            ]
        }

**target-account-queue-arn** : トリガーとして設定するSQSキューのArn
