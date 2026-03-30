## カスタムアクションでAPI URLの応答をチェック
### CodePipelineで検証用ステージを作成する
アクションプロバイダー:AWS Lambda

関数名:検証用Lambda

### Lambda関数(検証用)
```
import json
import os
import boto3
import requests

codepipeline = boto3.client('codepipeline')

URL = os.environ['API_URL']

def lambda_handler(event, context):
    try:
        # APIにGETリクエスト
        res = requests.get(URL)
        status_code = res.status_code
        print(f"API response status: {status_code}")

        # 成功時
        if status_code == 200:
            codepipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])
            return {
                'statusCode': status_code,
                'body': "Lambda execution completed"
            }
        else:
            # 失敗時
            codepipeline.put_job_failure_result(
                jobId=event['CodePipeline.job']['id'],
                failureDetails={
                    'type': 'JobFailed',
                    'message': f'API returned status code {status_code}',
                    'externalExecutionId': context.aws_request_id
                }
            )
            return {
                'statusCode': status_code,
                'body': "Lambda execution failed"
            }

    except Exception as e:
        print(f'Error occurred - {e}')
        # 例外発生時も失敗通知
        codepipeline.put_job_failure_result(
            jobId=event['CodePipeline.job']['id'],
            failureDetails={
                'type': 'JobFailed',
                'message': f'Exception occurred: {str(e)}',
                'externalExecutionId': context.aws_request_id
            }
        )
        return {
            'statusCode': 500,
            'body': "Lambda execution failed. Internal error occurred"
        }
```
