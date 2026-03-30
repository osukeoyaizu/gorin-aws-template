import json
import boto3
import os

sqs = boto3.client("sqs", region_name='ap-northeast-1')
QUEUE_URL = os.environ['QUEUE_URL']

def receive_message(queue_url):
    return sqs.receive_message(
        QueueUrl=queue_url,
        WaitTimeSeconds=1,
        # MaxNumberOfMessages=10
    )

def delete_message(queue_url, receiptHandle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receiptHandle
    )
    print("deleted message")

def lambda_handler(event, context):
    body_list = []
    max_iterations = 10  # 無限ループ防止

    for _ in range(max_iterations):
        response = receive_message(QUEUE_URL)

        if 'Messages' not in response:
            print("No more messages.")
            break

        for message in response['Messages']:
            try:
                # S3イベント通知の例
                # data = json.loads(message['Body'])
                # bucket = data['Records'][0]['s3']['bucket']['name']
                # key = data['Records'][0]['s3']['object']['key']
                # print(bucket, key)

                body_list.append(message['Body'])
                delete_message(QUEUE_URL, message['ReceiptHandle'])

            except Exception as e:
                print(f"Error processing message: {e}")
                continue

    print(body_list)

    return {
        'statusCode': 200,
        'body': json.dumps('Processed messages')
    }
