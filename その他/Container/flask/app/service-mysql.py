import os
import sys
import pymysql

DBName = 'database'
TableName = 'table'


def connection_mysql():
    rds_host = ""
    rds_username = "admin"
    rds_password = "Passw0rd"
    rds_dbname = DBName

    con = pymysql.connect(host=rds_host, user=rds_username, password=rds_password, db=rds_dbname)
    return con


# 全データ取得
def get_data():
    with con.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(f"SELECT * FROM {TableName}")
        data = cur.fetchall()
    return data


def get_data_byid(id):
    with con.cursor(pymysql.cursors.DictCursor) as cur:
        where_clause = f'id = {id}'
        cur.execute(f"SELECT * FROM {TableName} WHERE {where_clause}")
        data = cur.fetchall()
    return data


# 全データ(辞書型)取得
def get_dict_data():
    with con.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(f"SELECT * FROM {TableName}")
        dict_data = cur.fetchall()
    return dict_data


# データ登録
def post_data(data):
    sql = generate_insert_sql(TableName, data)
    with con.cursor() as cur:
        cur.execute(sql)
    con.commit()


# insert用のSQL文を作成
def generate_insert_sql(TableName, data):
    """辞書型のデータを元にSQLのINSERT文を生成する関数。"""
    columns = ', '.join(data.keys())  # カラム名
    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in data.values()])  # 値
    sql = f"INSERT INTO {TableName} ({columns}) VALUES ({values})"
    return sql

    
# データ更新
def update_data(con, data):
    id = data['id']
    where_clause = f'id = {id}'
    sql = generate_update_sql(TableName, data, where_clause)
    print(sql)

    with con.cursor() as cur:
        cur.execute(sql)
    con.commit()


# update用のSQL文を作成
def generate_update_sql(TableName, data, where_clause):
    """辞書型のデータを元にSQLのUPDATE文を生成する関数。"""
    set_clause = ', '.join([f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in data.items()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    return sql


# データ削除
def delete_data(con, data):
    id = data['id']
    where_clause = f'id = {id}'
    with con.cursor() as cur:
        sql = f"DELETE FROM {TableName} WHERE {where_clause}"
        cur.execute(sql)
        data = cur.fetchall()
    return data


con = connection_mysql()
