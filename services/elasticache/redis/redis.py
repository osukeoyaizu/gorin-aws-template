import json
import os
import boto3
import redis
import requests

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

    
# redis接続情報(転送中の暗号化有効)
def encrypted_connection_redis():
    secret = json.loads(get_secret())
    redis_host = secret['redis_host']
    redis_port = secret['redis_port']
    cache = redis.Redis(host=redis_host, port=redis_port, ssl=True, ssl_cert_reqs="none")
    return cache


# 辞書型で値を返す
def get_dict_data(key):
    response = requests.get(key)
    print(response.json())
    return response.json()


# キャッシュデータ取得
def check_cache(cache, key):
    response_data = cache.get(key)
    
    if response_data:
        print('Cache exists!')
        return response_data
    
    else:
        print('Cache not exists...')
        response_data = get_dict_data(key)

        # キャッシュを保存
        print('Cache setting')
        data = json.dumps(response_data, default=str) # timestampが含まれる場合は json.dumps(data, default=str)
        cache.set(key, data, ex=ttl)  # r.set(key, value_string ← json形式, ex=ttl)
        return data
    

def lambda_handler(event, context):
    id = event['id']

    # redis接続情報(転送中の暗号化有効)
    cache = encrypted_connection_redis()

    # キャッシュデータ取得
    key = f"https://tz75yjw0y8.execute-api.ap-northeast-1.amazonaws.com/dev/?id={id}"

    json_data = check_cache(cache, key)

    return {
        'statusCode': 200,
        'body':json_data
    }