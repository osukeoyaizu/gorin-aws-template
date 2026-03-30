import json
import boto3

kinesis = boto3.client("kinesis", region_name='ap-northeast-1')

# シャード取得
def list_shards(stream_name):
    shards = kinesis.list_shards(
        StreamName=stream_name
        )
    return shards


# イテレータ取得
def get_shard_iterator(stream_name, shards):
    iter_list = []
    for shard in shards["Shards"]:
        response = kinesis.get_shard_iterator(
            StreamName=stream_name, 
            ShardId=shard["ShardId"], 
            ShardIteratorType='TRIM_HORIZON'
        )
        iter_list.append(response)
    return iter_list


# レコード取得
def get_records(iter_list):
    response_list = []
    for iter in iter_list:
        response = kinesis.get_records(
            ShardIterator=iter['ShardIterator'],
            Limit=100
        )
        response_list.append(response)
    return response_list


def lambda_handler(event, context):
    stream_name = "lab2-stream"

    # シャード取得
    shards = list_shards(stream_name)

    # イテレータ取得
    iter_list = get_shard_iterator(stream_name, shards)

    # レコード取得
    response_list = get_records(iter_list)

    for records in response_list: 
        for record in records['Records']:
            data = record['Data'].decode('utf-8')
            print(data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
