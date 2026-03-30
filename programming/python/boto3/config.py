import json
import boto3
from botocore.config import Config
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
TABLE = 'oyaizu-table'
serializer = TypeSerializer()
deserializer = TypeDeserializer()

# connect_timeout: サーバーへの接続確立のタイムアウト
# read_timeout: 接続確立後の待機時間
# total_max_attempts: 合計最大試行回数
conf = Config(region_name="ap-northeast-1", connect_timeout=5, read_timeout=30, retries={"mode": "standard", "total_max_attempts": 1})
client = boto3.client(
    service_name='dynamodb',
    config=conf
)

def post_data(data):
    item = {
        k: serializer.serialize(v)
        for k, v in data.items()
    }
    options = {
        'TableName': TABLE,
        'Item': item,
    }
    response = client.put_item(**options)
    return data

def lambda_handler(event, context):
    data = json.loads(event['Records'][0]['body'])
    test_id = data['id']
    name = data['name']
    data = {
        "id": test_id,
        "name": name
    }
    response = post_data(data)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
