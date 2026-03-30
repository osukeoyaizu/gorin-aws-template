import json
import datetime
import boto3

transcribe = boto3.client('transcribe', region_name='ap-northeast-1')


def start_transcription_job(bucket, key, job_name, language_code, output_bucket, output_key):
    transcribe.start_transcription_job(
        TranscriptionJobName= job_name,
        LanguageCode=language_code,
        # 言語が不明な場合
        # IdentifyLanguage=True,   
        Media={
            'MediaFileUri': f"https://{bucket}.s3.ap-northeast-1.amazonaws.com/{key}"
        },
        OutputBucketName=output_bucket,
        OutputKey=output_key
    )


def lambda_handler(event, context):
    dt = str(int(datetime.datetime.now().timestamp()))

    bucket = 'sample-s3'
    key = 'sample.mp3'
    job_name = dt + '_Transcription'
    language_code = 'ja-JP'
    output_bucket = 'sample-output-s3'
    output_key = dt + '.json'

    start_transcription_job(bucket, key, job_name, language_code, output_bucket, output_key)  

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
