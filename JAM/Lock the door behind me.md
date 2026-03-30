## task1
### iamポリシー(SyslogS3AccessPolicy)編集
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::company-security-logs",
            "Effect": "Allow",
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "syslog/*"
                    ]
                }
            }
        },
        {
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::company-security-logs/syslog/*",
            "Effect": "Allow",
            "Condition": {
                "DateGreaterThan": {
                    "aws:CurrentTime": "2022-04-01T00:00:00Z"
                },
                "DateLessThan": {
                    "aws:CurrentTime": "2022-05-01T00:00:00Z"
                }
            }
        }
    ]
}
```


## task2
### iamポリシー(DynamoDbCustomerAccessPolicy)編集
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "dynamodb:Query",
            "Resource": "arn:aws:dynamodb:{Region}:{AccountId}:customers",
            "Effect": "Allow",
            "Condition": {
                "ForAllValues:StringEquals": {
                    "dynamodb:LeadingKeys": "Customer1234"
                }
            }
        }
    ]
}
```

## task3
### iamポリシー(EmployeeDataAccessPolicy)編集
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "dynamodb:Query",
            "Resource": "arn:aws:dynamodb:{Region}:{AccountId}:employees",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "aws:PrincipalTag/EmployeeDataAccess": "yes"
                }
            }
        }
    ]
}
```
