import json
import os
import boto3
import pymemcache
import requests
from botocore.config import Config
import ssl
import base64

REGION_NAME = os.environ['REGION_NAME']
SECRETS_NAME = os.environ['SECRETS_NAME']

ttl = 20

# シークレット取得
def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=SECRETS_NAME
    )

    secret = get_secret_value_response['SecretString']
    return secret

    
def encrypted_connection_memcached():
    secret = json.loads(get_secret())
    memcached_host = secret['memcached_host']
    memcached_port = secret['memcached_port']
    context = ssl.create_default_context()
    cache = pymemcache.Client((memcached_host, memcached_port), tls_context=context)
    return cache


# 辞書型で値を返す
def get_dict_data(url):
    response = requests.get(url)
    print(response.json())
    return response.json()


# キャッシュデータ取得
def check_cache(cache, key):
    url = key
    key = base64.b64encode(key.encode())
    response_data = cache.get(key)

    if response_data:
        print('Cache exists!')
        return response_data
    
    else:
        print('Cache not exists...')
        response_data = get_dict_data(url)

        # キャッシュを保存
        print('Cache setting')
        data = json.dumps(response_data, default=str) # timestampが含まれる場合は json.dumps(data, default=str)
        cache.set(key, data, expire=ttl, noreply=False)
        return data
    

def lambda_handler(event, context):
    # キーに数値型は指定できない
    id = str(event['id'])

    # redis接続情報(転送中の暗号化有効)
    cache = encrypted_connection_memcached()

    key = f"https://bw0nzwuet9.execute-api.ap-northeast-1.amazonaws.com/dev?id={id}"
    # キャッシュデータ取得
    json_data = check_cache(cache, key)

    return {
        'statusCode': 200,
        'body':json_data
    }