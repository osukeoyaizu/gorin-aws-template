import json
import boto3
import datetime

sns = boto3.client('sns',region_name='ap-northeast-1')
topic_arn = 'arn:aws:sns:ap-northeast-1:157094121738:lab2-sns'
fifo_topic_arn = 'arn:aws:sns:ap-northeast-1:157094121738:lab2-sns.fifo'

def publish(topic_arn, message):
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return response

def fifo_publish(topic_arn, message):
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageDeduplicationId=datetime.datetime.now().isoformat(),
        MessageGroupId='Group1'
    )
    return response

def lambda_handler(event, context):
    message = 'test message'

    publish_response = publish(topic_arn, message)

    fifo_publish_response = fifo_publish(fifo_topic_arn, message)

    return {
        'statusCode': 200,
        'body': json.dumps(fifo_publish_response)
    }
