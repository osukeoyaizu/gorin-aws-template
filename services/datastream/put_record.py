import boto3
import json
import random
import string
import datetime

stream_name = "lab2-stream"
kinesis = boto3.client("kinesis", region_name='ap-northeast-1')


def make_data(i):
    data = {}
    now = datetime.datetime.now()
    data["id"] = "device%s" % (i)
    data["timestamp"] = int(now.timestamp() * 1000)
    data["spot"] = random.choice(list(string.ascii_uppercase))
    data["temperature"] = random.randint(10, 40)
    return data


def put_record(data, p_key):
    kinesis.put_record(
        StreamName=stream_name,
        Data=data,
        PartitionKey=p_key
        )


if __name__ == "__main__":
    for i in range(0,100):
        data = json.dumps(make_data(i))
        p_key = str(random.randint(1, 100))
        # Kinesisへレコード送信
        put_record(data, p_key)
