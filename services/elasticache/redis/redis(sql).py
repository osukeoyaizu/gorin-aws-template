import json
import os
import boto3
import pymysql
import redis

rds_host = os.environ['RDS_HOST']
rds_username = os.environ['RDS_USER']
rds_password = os.environ['RDS_PASSWORD']
rds_dbname = os.environ['RDS_DB']
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']

# 編集データ
table_name = 'analytics'
sql = 'select * from ' + table_name
ttl = 10


# データベース接続
def connection_mysql():
    con = pymysql.connect(host=rds_host, user=rds_username, password=rds_password, database=rds_dbname)
    return con


# # redis接続
# def connection_redis():
#     cache = redis.Redis(host=redis_host, port=redis_port, db=0)
#     return cache

    
# redis接続情報(転送中の暗号化有効)
def encrypted_connection_redis():
    cache = redis.Redis(host=redis_host, port=redis_port, ssl=True, ssl_cert_reqs="none", ssl_check_hostname=False )
    return cache


# 辞書型で値を返す
def get_dict_data(con, sql):
    with con.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql)
        dict_data = cur.fetchall()
    return dict_data


# キャッシュデータ取得
def check_cache(cache, con):
    response_data = cache.get(sql)
    
    if response_data:
        print('Cache exists!')
        return response_data
    
    else:
        print('Cache not exists...')
        response_data = get_dict_data(con, sql)

        # キャッシュを保存
        print('Cache setting')
        data = json.dumps(response_data, default=str) # timestampが含まれる場合は json.dumps(data, default=str)
        cache.set(sql, data, ex=ttl)  # r.set(key, value_string ← json形式, ex=ttl)
        return data
    

def lambda_handler(event, context):
    # データベース接続
    con = connection_mysql()

    # # redis接続
    # cache = connection_redis()

    # redis接続情報(転送中の暗号化有効)
    cache = encrypted_connection_redis()

    # キャッシュデータ取得
    json_data = check_cache(cache, con)

    return {
        'statusCode': 200,
        'body':json_data
    }
