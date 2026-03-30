import json
import boto3

polly = boto3.client('polly', region_name='ap-northeast-1')
s3 = boto3.client('s3')

# 文字列 → 音声
def synthesize_speech(language_code, text):
    response = polly.synthesize_speech(
        Engine='standard',
        LanguageCode=language_code,
        OutputFormat="mp3",
        Text=text,
        TextType='text',
        VoiceId="Mizuki"
    )
    return response

# S3に保存
def put_object(bucket, key, body):
    response = s3.put_object(Bucket=bucket, Key=key ,Body=body)
    return response


def lambda_handler(event, context):
    language_code = 'ja-JP'
    text = 'おはようございます'

    # 文字列 → 音声
    synthesize_speech_response = synthesize_speech(language_code, text)

    # 音声データを取得
    audio_stream = synthesize_speech_response['AudioStream'].read()


    bucket = 'your-s3-bucket-name'
    key = 'speech.mp3'
    put_object(bucket, key, audio_stream)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Audio saved to s3://{bucket}/{key}')
    }
