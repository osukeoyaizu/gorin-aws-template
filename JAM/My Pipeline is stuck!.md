## task1
### IAMロール(challenge-lambda-role)のIAMポリシー(policy)に以下のステートメント追加
```
{
    "Sid": "Statement1",
    "Effect": "Allow",
    "Action": [
        "codepipeline:*"
    ],
    "Resource": ["*"]
}
```

### コード編集
```
import ssl
import os
import boto3
from urllib.request import Request, urlopen

import pipeline_utils

ssl._create_default_https_context = ssl._create_unverified_context

codepipeline = boto3.client('codepipeline')

def lambda_handler(event, context):
    req = Request(os.getenv('API_URL'))
    try:
        token = pipeline_utils.get_token()
        req.add_header('Authorization', token)
        status_code = urlopen(req).getcode()
        print(status_code)
        codepipeline.put_job_success_result(jobId = event['CodePipeline.job']['id'])
        return {
            'statusCode': status_code,
            'body': "Lambda execution completed"
        }
    except Exception as e:
        print(f'Error occurred - {e}')
        return {
            'statusCode': 500,
            'body': "Lambda execution failed. Internal error occurred"
        }

```
