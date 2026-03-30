import time
import json
import os
import boto3

sqs = boto3.client("sqs", region_name='ap-northeast-1')
QUEUE_URL = os.environ['QUEUE_URL']
FIFO_QUEUE_URL = os.environ['FIFO_QUEUE_URL']


def send_message(queue_url, message):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )


def fifo_send_message(fifo_queue_url, message):
    response = sqs.send_message(
        QueueUrl=fifo_queue_url,
        MessageBody=message,
        MessageDeduplicationId=str(time.time_ns()),    #MessageDeduplicationId=str(time.time_ns())でも可
        MessageGroupId='Group1'
    )


def lambda_handler(event, context):
    message = {
        "id": "1",
        "text": "text01"
    }
    message = json.dumps(message)

    send_message(QUEUE_URL, message)

    fifo_send_message(FIFO_QUEUE_URL, message)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }