## 動的ポリシーを使ったテナント分離
### TENANT_ROLEの信頼ポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "<LambdaのロールARN>"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
**※与える権限よりも大きい権限をアタッチしておく必要がある**

### Lambda関数
```
import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['TABLE_NAME']
ACCOUNT_ID = os.environ['ACCOUNT_ID']
TENANT_ROLE = os.environ['TENANT_ROLE']
REGION = os.environ['REGION']

def lambda_handler(event, context):
    cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
    queryStringParameters = event['queryStringParameters']
    userId = queryStringParameters['userId']

    policy_document = {
        'Version': '2012-10-17',
        'Statement': [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:Query"
                ],
                "Resource": [
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT_ID}:table/{TABLE_NAME}"
                ],
                "Condition": {
                    "ForAllValues:StringEquals": {
                        "dynamodb:LeadingKeys": [
                            cognito_username
                        ]
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": "kms:*",
                "Resource": "*"
            }
        ]
    }
    
    sts = boto3.client('sts')
    credential = sts.assume_role(
        RoleArn=f'arn:aws:iam::{ACCOUNT_ID}:role/{TENANT_ROLE}',
        RoleSessionName=f"oyaizu-session-{str(uuid.uuid4())}", 
        Policy=json.dumps(policy_document),
    )['Credentials']
 
    session = boto3.Session(
        aws_access_key_id=credential['AccessKeyId'],
        aws_secret_access_key=credential['SecretAccessKey'],
        aws_session_token=credential['SessionToken'],
    )

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    try:
        response = table.query(
            KeyConditionExpression=Key('UserId').eq(userId)
        )
        result_list = []
        for item in response['Items']:
            print(item)
            result_dict = {}
            result_dict['userId'] = item['UserId']
            result_dict['timestamp'] = item['Timestamp']
            result_dict['score'] = item['Score']
            result_list.append(result_dict)

    except ClientError as e:
        print(e)
        if e.response['Error']['Code'] == "AccessDeniedException":
            return {
                'statusCode': 403,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'https://d1rleioipw53je.cloudfront.net',
                    'Access-Control-Allow-Methods': 'GET'
                },
                'body': json.dumps({"error": "Forbidden"})
            }       

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://d1rleioipw53je.cloudfront.net',
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': json.dumps(result_list, default=str)
    }
```
