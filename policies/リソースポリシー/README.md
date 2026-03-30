## ECR
### VPCあり
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "AccessViaVPCEndpointOnly",
        "Action": "ecr:*",
        "Effect": "Allow",
        "Principal": "*",
        "Condition": {
            "StringEquals": {
            "aws:SourceVpce": [
                "<vpc-endpoint-id(ecr.dkr)>",
                "<vpc-endpoint-id(ecr.api)>"
            ]
            }
        }
        }
    ]
}
```
**vpc-endpoint-id(ecr.dkr)**: 許可するVPCエンドポイントのID(ecr.dkr)
**vpc-endpoint-id(ecr.api)**: 許可するVPCエンドポイントのID(ecr.api)

### VPCなし
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRRepositoryPolicy",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:root"
      },
      "Action": "ecr:*"
    }
  ]
}
```

## S3
```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Sid": "RestrictToTLSRequestsOnly",
        "Action": "s3:*",
        "Effect": "Deny",
        "Resource": [
            "arn:aws:s3:::<bucket-name>",
            "arn:aws:s3:::<bucket-name>/*"
        ],
        "Condition": {
            "Bool": {
                "aws:SecureTransport": "false"
            }
        },
        "Principal": "*"
    }]
}
```

## DynamoDB
### VPCあり
```
{
  "Version": "2012-10-17",
  "Id": "PolicyId",
  "Statement": [
    {
      "Sid": "AccessToSpecificVPCEOnly",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "dynamodb:*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:sourceVpce": "<vpc-endpoint-id>"
        }
      }
    }
  ]
}
```
### VPCなし
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::<account-id>:root"
			},
			"Action": [
				"dynamodb:*"
			],
			"Resource": [
				"arn:aws:dynamodb:<region>:<account-id>:table/<table>"
			]
		}
	]
}
```

## APIGateway
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "*"
    }
  ]
}
```


## SecretsManager
```
{
"Id": "example-policy-1",
"Version":"2012-10-17",		 	 	 
"Statement": [
{
  "Sid": "RestrictGetSecretValueoperation",
  "Effect": "Allow",
  "Principal": "*",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "aws:sourceVpce": "<vpc-endpoint-id>"
    }
  }
}
]
}

```