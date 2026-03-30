import json
import os
import base64
import boto3
import ssl
import pymysql
import pymemcache


rds_host = os.environ['RDS_HOST']
rds_username = os.environ['RDS_USER']
rds_password = os.environ['RDS_PASSWORD']
rds_dbname = os.environ['RDS_DB']
memcached_host = os.environ['MEMCACHED_HOST']
memcached_port = os.environ['MEMCACHED_PORT']

# 編集データ
table_name = 'analytics'
sql = 'select * from ' + table_name
sql_key = base64.b64encode(sql.encode())
ttl = 10


# データベース接続
def connection_mysql():
    con = pymysql.connect(host=rds_host, user=rds_username, password=rds_password, database=rds_dbname)
    return con


# # memcached接続
# def connection_memcached():
#     cache = pymemcache.Client((memcached_host, memcached_port))
#     return cache

    
# memcached接続情報(転送中の暗号化有効)
def encrypted_connection_memcached():
    context = ssl.create_default_context()
    cache = pymemcache.Client((memcached_host, memcached_port), tls_context=context)
    return cache


# 辞書型で値を返す
def get_dict_data(con, sql):
    with con.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql)
        dict_data = cur.fetchall()
    return dict_data


# キャッシュデータ取得
def check_cache(cache, con):
    response_data = cache.get(sql_key)
    
    if response_data:
        print('Cache exists!')
        return response_data
    
    else:
        print('Cache not exists...')
        response_data = get_dict_data(con, sql)

        # キャッシュを保存
        print('Cache setting')
        data = json.dumps(response_data, default=str) # timestampが含まれる場合は json.dumps(data, default=str)
        cache.set(sql_key, data, expire=ttl, noreply=False)
        return data
    

def lambda_handler(event, context):

    # データベース接続
    con = connection_mysql()

    # # memcached接続
    # cache = connection_memcached()

    # memcached接続情報(転送中の暗号化有効)
    cache = encrypted_connection_memcached()

    # キャッシュデータ取得
    json_data = check_cache(cache, con)

    return {
        'statusCode': 200,
        'body':json_data
    }
