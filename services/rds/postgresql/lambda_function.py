import json
import boto3
import os
import psycopg2, psycopg2.extras

REGION_NAME = os.environ['REGION_NAME']
SECRETS_NAME = os.environ['SECRETS_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

PRIMARY_KEY = 'id'


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


# データベース接続
def connection_postgresql():
    # シークレット取得
    secret = json.loads(get_secret())
    print(secret)
    rds_host = secret['host']
    rds_username = secret['username']
    rds_password = secret['password']
    rds_dbname = secret['dbname']

    con = psycopg2.connect(host=rds_host, user=rds_username, password=rds_password, database=rds_dbname)
    return con


# 全データ取得
def get_data(con):
    with con.cursor() as cur:
        sql = f"SELECT * FROM {TABLE_NAME}"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
    return data


# 全データ(リスト型)取得
def get_data_list(con):
    with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        sql = f"SELECT * FROM {TABLE_NAME}"
        cur.execute(sql)
        dict_data = cur.fetchall()
    return dict_data


# idに一致したデータを取得
def get_data_byid(con, id):
    with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        where_clause = f"{PRIMARY_KEY} = {id}"
        sql = f"SELECT * FROM {TABLE_NAME} WHERE {where_clause}"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
    return data


# データ登録
def insert_data(con, dictionary):
    sql = generate_insert_sql(TABLE_NAME, dictionary)
    print(sql)
    with con.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
    con.commit()
    return result


# insert用のSQL文を作成
def generate_insert_sql(table_name, data):
    """辞書型のデータを元にSQLのINSERT文を生成する関数。"""
    columns = ', '.join(data.keys())  # カラム名
    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in data.values()])  # 値
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING {PRIMARY_KEY};"
    return sql

    
# データ更新
def update_data(con, dictionary):
    id = dictionary[PRIMARY_KEY]
    where_clause = f"{PRIMARY_KEY} = {id}"
    del dictionary[PRIMARY_KEY]
    sql = generate_update_sql(TABLE_NAME, dictionary, where_clause)
    print(sql)
    with con.cursor() as cur:
        cur.execute(sql)
    con.commit()


# update用のSQL文を作成
def generate_update_sql(table_name, data, where_clause):
    """辞書型のデータを元にSQLのUPDATE文を生成する関数。"""
    set_clause = ', '.join([f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in data.items()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    return sql


# データ削除
def delete_data(con, dictionary):
    id = dictionary[PRIMARY_KEY]
    where_clause = f"{PRIMARY_KEY} = {id}"
    with con.cursor() as cur:
        sql = f"DELETE FROM {TABLE_NAME} WHERE {where_clause}"
        print(sql)
        cur.execute(sql)
    con.commit()


def lambda_handler(event, context):
    # データベース接続
    con = connection_postgresql()

    # 全データ取得
    data = get_data(con)

    # 全データ(リスト型)取得
    data_list = get_data_list(con)

    # idに一致したデータを取得
    id = 1
    data_byid = get_data_byid(con, id)

    # データ登録
    post_item = {}
    post_item['text'] = 'sample'
    post_result = insert_data(con, post_item)

    # 最後に登録したデータのidを取得
    last_insert_id = post_result[0][0]

    # データ更新
    put_item = {}
    put_item['id'] = '1'
    put_item['text'] = 'sample'
    update_data(con, put_item)

    # データ削除
    delete_item = {}
    delete_item['id'] = '1'
    delete_data(con, delete_item)

    return {
        'statusCode': 200,
        'body': json.dumps(data_list, default=str)  # timestampが含まれる場合は json.dumps(data, default=str)
    }
