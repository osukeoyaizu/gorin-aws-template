import boto3
import json
import random
import string
import datetime

stream_name = "lab2-firehose"
firehose = boto3.client("firehose", region_name='ap-northeast-1')

def make_data(i):
    data = {}
    now = datetime.datetime.now()
    data["id"] = "device%s" % (i)
    data["timestamp"] = int(now.timestamp() * 1000)
    data["spot"] = random.choice(list(string.ascii_uppercase))
    data["temperature"] = random.randint(10, 40)
    return data


def put_record(data):
    firehose.put_record(
        DeliveryStreamName=stream_name,
        Record ={
            'Data': data
        }
    )


def lambda_handler(event, context):

    for i in range(0,100):
        data = json.dumps(make_data(i))

        # firehoseへレコード送信
        put_record(data)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
