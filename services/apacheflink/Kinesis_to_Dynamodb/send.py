import json
import boto3
import random
import string
import datetime

# InputSteam名
STREAM_NAME = "lab1-stream"

def get_data():
    EVENT_TIME = datetime.datetime.now().timestamp()
    SPOT = random.choice(list(string.ascii_uppercase))
    TEMPERATURE = random.randint(10, 40)
    HUMIDITY = random.uniform(0, 100)
    IS_ACTIVE = random.choice([True, False])

    data = {}
    data['EVENT_TIME'] = EVENT_TIME
    data['SPOT'] = SPOT
    data['TEMPERATURE'] = TEMPERATURE
    data['HUMIDITY'] = HUMIDITY
    data['IS_ACTIVE'] = IS_ACTIVE

    return data




def generate(stream_name, kinesis_client):
    time = 0

    while True:
        data = get_data()
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey="partitionkey")

        print(f"Sent data: {data}")  # デバッグ用に送信データを表示
        time += 1

if __name__ == '__main__':
    generate(STREAM_NAME, boto3.client('kinesis', region_name='ap-northeast-1'))