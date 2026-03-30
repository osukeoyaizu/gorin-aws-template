import json
import boto3
import io
import zipfile
import os
import logging

s3 = boto3.client('s3')
codepipeline = boto3.client('codepipeline')

PIPELINE_NAME = os.environ['PIPELINE_NAME'] 
INPUT_BUCKET = os.environ['INPUT_BUCKET']
ROLE_ARN = os.environ['ROLE_ARN']
EVENT_RULE_NAME = os.environ['EVENT_RULE_NAME']

def lambda_handler(event, context):
    print(json.dumps(event, default=str))
    jobId = event["CodePipeline.job"]['id']
    output_bucket = ''
    executionId = ''
    try:
        response = codepipeline.get_pipeline_state(name=PIPELINE_NAME)
        print(json.dumps(response, default=str))
        for stageState in response['stageStates']:
            if stageState['stageName'] == 'ETL':
                for actionState in stageState['actionStates']:
                    if actionState['actionName'] == 'Lambda_ETL':
                        executionId = stageState['latestExecution']['pipelineExecutionId']
        
        if executionId == '':
            raise Exception("executionId not found")

        inputArtifacts = event["CodePipeline.job"]["data"]["inputArtifacts"]
        for inputArtifact in inputArtifacts:
            if inputArtifact['name'] == 'Source_ETL':
                s3Location = inputArtifact['location']['s3Location']
                output_bucket = s3Location['bucketName']
                _object = s3.get_object(Bucket=output_bucket, Key=s3Location['objectKey'])
                zip_bytes = _object['Body'].read()
                with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as z:
                    for file in z.infolist():
                        if file.filename == 'preprocess.py':
                            s3.put_object(Bucket=output_bucket, Key=f"{executionId}/code/{file.filename}", Body=z.read(file))
                        if file.filename == 'etljob.json':
                            etlJob = json.loads(z.read('etljob.json').decode('ascii'))
        codepipeline.put_job_success_result(jobId=jobId)
    except Exception as e:
        print(e)
        resppnse = codepipeline.put_job_failure_result(
            jobId=jobId,
            failureDetails={
                'type': 'ConfigurationError',
                'message': str(e),
                'externalExecutionId': context.aws_request_id
            }
        )
 
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
