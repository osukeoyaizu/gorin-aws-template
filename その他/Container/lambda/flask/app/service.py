import json
import boto3
import os
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

TABLE = os.environ['TABLE']
REGION = os.environ['REGION']
PARTITION_KEY = 'id'

dynamo = boto3.client('dynamodb', region_name=REGION)

serializer = TypeSerializer()
deserializer = TypeDeserializer()

# 全件取得
def get_data():
    options = {
        'TableName': TABLE,
    }
    response = dynamo.scan(**options)
    data = []
    for item in response['Items']:
        deserized_item = {
            k: deserializer.deserialize(v)
            for k, v in item.items()
        }
        data.append(deserized_item)
    return data


# idに一致したデータを取得
def get_data_byid(id):
    options = {
        'TableName': TABLE,
        'Key': {
            PARTITION_KEY : {'N': id},
            # SORT_KEY: {'S': sort_key}, # ソートキーがある場合(引数追加)
        }
    }
    response = dynamo.get_item(**options)
    
    if response.get('Item'):
        data = {
            k: deserializer.deserialize(v)
            for k, v in response['Item'].items()
        }
        return data
    
    else:
        return None
    

# データ登録
def post_data(data):
    item = {
        k: serializer.serialize(v)
        for k, v in data.items()
    }
    options = {
        'TableName': TABLE,
        'Item': item,
    }
    response = dynamo.put_item(**options)
    return data


# データ更新
def put_data(data):
    # 更新する項目の設定
    item = {
        k: serializer.serialize(v)
        for k, v in data.items()
    }
    # 更新する項目の設定
    update_expression = "SET "
    expression_attribute_values = {}

    for key, value in item.items():
        # # ソートキーがある場合
        # if key == PARTITION_KEY or key == SORT_KEY: 
        #     continue
        if key == PARTITION_KEY:
            continue
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = value

    # 最後のカンマを削除
    update_expression = update_expression[:-2]

    options = {
        'TableName': TABLE,
        'Key': {
            PARTITION_KEY: {'S': data[PARTITION_KEY]},
            # SORT_KEY: {'S': data[SORT_KEY]}, # ソートキーがある場合
        },
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': expression_attribute_values,
        'ReturnValues': 'ALL_NEW'
    }
    response = dynamo.update_item(**options)
    return data


# データ削除
def delete_data(id):
    options = {
        'TableName': TABLE,
        'Key': {
            PARTITION_KEY: {'S': id},
            # SORT_KEY: {'S': sort_key}, # ソートキーがある場合(引数追加)
        }
    }
    response = dynamo.delete_item(**options)
    return id
