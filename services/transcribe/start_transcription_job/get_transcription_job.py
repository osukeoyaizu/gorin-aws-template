import json
import boto3
import datetime
import time

transcribe = boto3.client('transcribe', region_name='ap-northeast-1')

s3 = boto3.client('s3')

# ジョブ開始
def start_transcription_job(mediaFileUri, job_name, language_code, output_bucket, output_key):
    transcribe.start_transcription_job(
        TranscriptionJobName= job_name,
        LanguageCode=language_code,
        # # 言語が不明な場合
        # IdentifyLanguage=True,   
        Media={
            'MediaFileUri': mediaFileUri
        },
        OutputBucketName=output_bucket,
        OutputKey=output_key
    )


# ジョブの情報を取得する
def get_transcription_job(job_name):
    response = transcribe.get_transcription_job(
        TranscriptionJobName=job_name
    )
    return response


# ファイルの内容を読む
def get_object(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response
    

def lambda_handler(event, context):
    region = 'ap-northeast-1'
    dt = str(int(datetime.datetime.now().timestamp() * 1000))
    bucket = 'sample-s3'
    key = 'sample.mp3'
    job_name = dt + '_Transcription'
    language_code = 'ja-JP'
    output_bucket = 'sample-output-s3'
    output_key = dt + '.json'
    mediaFileUri =  f"https://{bucket}.s3.{region}.amazonaws.com/{key}"

    start_transcription_job(mediaFileUri, job_name, language_code, output_bucket, output_key)
    
    while True:
        get_transcription_job_response = get_transcription_job(job_name)
        if get_transcription_job_response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(5)

    # ジョブが失敗した場合
    if get_transcription_job_response['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
        raise Exception('Transcribeジョブが失敗しました')
    
    # ファイルの内容を読む
    get_object_response = get_object(output_bucket, output_key)
    body = get_object_response['Body'].read()
    decoded_body = json.loads(body.decode())
    transcribed_text = decoded_body['results']['transcripts'][0]['transcript']
    print(transcribed_text)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }