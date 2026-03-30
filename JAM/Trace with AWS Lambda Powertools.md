## task1
Lambda関数(GetUser)を実行して回答を取得する

## task2
Lambda関数(GetUser)でX-Rayでのトレースを有効化してトレースIDを回答する

## task3
Lambda関数(GetUser)でPowerToolsのレイヤーを追加する
```
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

from aws_lambda_powertools import Tracer
tracer = Tracer(service="jam")

table_name = os.environ["TABLE_NAME"]
client = boto3.client("dynamodb")


def get_user(id):
    response = client.get_item(TableName=table_name, Key={"id": {"S": id}})
    return response["Item"]


def deserialise(item):
    d = TypeDeserializer()
    return {k: d.deserialize(v) for k, v in item.items()}


@tracer.capture_lambda_handler
def handler(event, context):
    item = get_user("jammer")
    user = deserialise(item)
    return user
```
