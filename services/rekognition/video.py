# 動画からラベルと有名人を取得する

import boto3
import json
import time

rekognition = boto3.client('rekognition', region_name='ap-northeast-1')

def start_label_detection(bucket, key):
    response = rekognition.start_label_detection(
        Video={'S3Object': {'Bucket': bucket, 'Name': key}},
        MinConfidence=80,
        NotificationChannel={
            'SNSTopicArn': 'arn:aws:sns:ap-northeast-1:xxxxxxyyyyyy:lab1',
            'RoleArn': 'arn:aws:iam::xxxxxxyyyyyy:role/RekognitionRole'
        }
    )
    return response['JobId']


def get_label_detection(job_id, max_wait=600, interval=10):
    elapsed = 0
    while elapsed < max_wait:
        response = rekognition.get_label_detection(JobId=job_id, SortBy='TIMESTAMP')
        status = response['JobStatus']
        print(f"Job status: {status}")
        if status in ['SUCCEEDED', 'FAILED']:
            return response
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError("Label detection job did not finish in time.")


def start_celebrity_recognition(bucket, key):
    response = rekognition.start_celebrity_recognition(
        Video={'S3Object': {'Bucket': bucket, 'Name': key}},
        NotificationChannel={
            'SNSTopicArn': 'arn:aws:sns:ap-northeast-1:xxxxxxyyyyyy:lab1',
            'RoleArn': 'arn:aws:iam::xxxxxxyyyyyy:role/RekognitionRole'
        }
    )
    return response['JobId']


def get_celebrity_recognition(job_id, max_wait=600, interval=10):
    elapsed = 0
    while elapsed < max_wait:
        response = rekognition.get_celebrity_recognition(JobId=job_id)
        status = response['JobStatus']
        print(f"Job status: {status}")
        if status in ['SUCCEEDED', 'FAILED']:
            return response
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError("Celebrity recognition job did not finish in time.")


def s3_event_sqs(event):
    data = json.loads(event['Records'][0]['body'])
    bucket = data['Records'][0]['s3']['bucket']['name']
    key = data['Records'][0]['s3']['object']['key']
    return bucket, key


def lambda_handler(event, context):
    bucket, key = s3_event_sqs(event)

    # 1. ジョブ開始
    label_job_id = start_label_detection(bucket, key)
    print(f"Started label detection job: {label_job_id}")

    # 2. 完了まで待機して結果取得
    result = get_label_detection(label_job_id)

    # 3. 検出結果を整形
    labels = []
    for label_detection in result.get('Labels', []):
        label = label_detection['Label']
        labels.append({
            'Name': label['Name'],
            'Confidence': label['Confidence'],
            'Timestamp': label_detection['Timestamp']
        })


    # 1. ジョブ開始
    celebrity_job_id = start_celebrity_recognition(bucket, key)
    print(f"Started celebrity recognition job: {celebrity_job_id}")

    # 2. 完了まで待機して結果取得
    result = get_celebrity_recognition(celebrity_job_id)

    # 3. 検出結果を整形
    celebrities = []
    for celeb in result.get('Celebrities', []):
        celebrities.append({
            'Name': celeb['Celebrity']['Name'],
            'Confidence': celeb['Celebrity']['Confidence'],
            'Timestamp': celeb['Timestamp']
        })


    print(json.dumps(labels, indent=2))
    print(json.dumps(celebrities, indent=2))


    return {
        'statusCode': 200,
        'body': json.dumps({'LabelJobId': label_job_id, 'CelebrityJobId': celebrity_job_id, 'Labels': labels, 'Celebrities': celebrities})
    }