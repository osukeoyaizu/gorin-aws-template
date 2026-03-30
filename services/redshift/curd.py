
import json
import boto3
import os
import time

REGION_NAME = os.environ['REGION_NAME']
SECRETS_NAME = os.environ['SECRETS_NAME']
DATABASE_NAME = os.environ['DATABASE_NAME']
SCHEMA_NAME = os.environ['SCHEMA_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

PRIMARY_KEY = 'id'

redshift = boto3.client('redshift-data')

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


# クエリ実行
def query_execution(sql):
    # シークレット取得
    secret = json.loads(get_secret())
    username = secret['username']
    database = secret['dbname']
    dbClusterIdentifier = secret['dbClusterIdentifier']

    result = redshift.execute_statement(
        ClusterIdentifier=dbClusterIdentifier,
        Database=database,
        DbUser=username,
        Sql=sql
    )

    # # クエリエディタで以下のSQLを実行して権限付与
    # # GRANT  ALL  ON DATABASE <データベース> TO "IAMR:<Lambdaのロール名>"
    # # GRANT  ALL  ON SCHEMA <データベース>.<スキーマ> TO "IAMR:<Lambdaのロール名>"
    # # GRANT  ALL  ON TABLE <データベース>.<スキーマ>.<テーブル> TO "IAMR:<Lambdaのロール名>"
    # result = redshift.execute_statement(
    #     WorkgroupName='workgroup',
    #     Database=database,
    #     Sql=sql
    # )

    # 実行IDを取得
    statement_id = result['Id']
    # クエリが終わるのを待つ
    while True:
        statement = redshift.describe_statement(Id=statement_id)
        print(statement)
        status = statement.get('Status')

        if status in ['FINISHED', 'FAILED', 'ABORTED']:
            break
        time.sleep(1)
        
    # ③クエリ結果返信（取得）
    try:
        if status == 'FINISHED':
            if int(statement['ResultSize']) > 0:
                # 結果取得
                result = redshift.get_statement_result(Id=statement_id)
                column_info = result['ColumnMetadata']
                records = result['Records']

                # カラム名の抽出
                column_names = [col['name'] for col in column_info]

                # レコードを dict に変換
                result_dicts = []
                for record in records:
                    row = {}
                    for col_name, col_value in zip(column_names, record):
                        # 値は辞書型で格納されているため、型に応じて取得
                        value = list(col_value.values())[0] if col_value else None
                        row[col_name] = value
                    result_dicts.append(row)

                return result_dicts
            else:
                raise Exception("戻り値がありません。")
        elif status == 'FAILED':
            raise Exception("処理に失敗しました。")
        elif status == 'ABORTED':
            raise Exception("処理を中断しました。")
    except Exception as e:
        print(e)


# 全データ取得
def get_data():
    sql = f'SELECT * FROM "{DATABASE_NAME}"."{SCHEMA_NAME}"."{TABLE_NAME}"'
    print(sql)
    result = query_execution(sql)
    return result


# idに一致したデータを取得
def get_data_byid(id):
    where_clause = f'"{PRIMARY_KEY}" = {id}'
    sql = f'SELECT * FROM "{DATABASE_NAME}"."{SCHEMA_NAME}"."{TABLE_NAME}" WHERE {where_clause}'
    print(sql)
    result = query_execution(sql)
    return result


# データ登録
def insert_data(dictionary):
    sql = generate_insert_sql(TABLE_NAME, dictionary)
    print(sql)
    result = query_execution(sql)
    return result


# insert用のSQL文を作成
def generate_insert_sql(table_name, data):
    """辞書型のデータを元にSQLのINSERT文を生成する関数。"""
    # カラムはダブルクォートで囲む
    columns = ', '.join([f'"{col}"' for col in data.keys()])
    # 文字列は単一引用符で囲む（※エスケープは必要に応じて追加）
    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in data.values()])
    sql = f'INSERT INTO "{DATABASE_NAME}"."{SCHEMA_NAME}"."{table_name}" ({columns}) VALUES ({values})'
    return sql


# データ更新
def update_data(dictionary):
    id = dictionary[PRIMARY_KEY]
    where_clause = f'"{PRIMARY_KEY}" = {id}'
    del dictionary[PRIMARY_KEY]
    sql = generate_update_sql(TABLE_NAME, dictionary, where_clause)
    print(sql)
    result = query_execution(sql)
    return result


# update用のSQL文を作成
def generate_update_sql(table_name, data, where_clause):
    """辞書型のデータを元にSQLのUPDATE文を生成する関数。"""
    # SET句のカラムもダブルクォート
    set_clause = ', '.join([f'"{key}" = \'{value}\'' if isinstance(value, str) else f'"{key}" = {value}' for key, value in data.items()])
    sql = f'UPDATE "{DATABASE_NAME}"."{SCHEMA_NAME}"."{table_name}" SET {set_clause} WHERE {where_clause}'
    return sql


# データ削除
def delete_data(dictionary):
    id = dictionary['id']
    where_clause = f'"id" = {id}'
    sql = f'DELETE FROM "{DATABASE_NAME}"."{SCHEMA_NAME}"."{TABLE_NAME}" WHERE {where_clause}'
    print(sql)
    result = query_execution(sql)
    return result


def lambda_handler(event, context):
    # 全データ取得
    data = get_data()

    # idに一致したデータを取得
    id = 1
    data_byid = get_data_byid(id)[0]

    # データ登録
    post_item = {}
    post_item['text'] = 'sample'
    insert_data(post_item)

    # データ更新
    put_item = {}
    put_item[PRIMARY_KEY] = '1'
    put_item['text'] = 'sample'
    update_data(put_item)

    # データ削除
    delete_item = {}
    delete_item[PRIMARY_KEY] = '1'
    delete_data(delete_item)

    return {
        'statusCode': 200,
        'body': json.dumps(data, default=str)  # timestampが含まれる場合は json.dumps(data, default=str)
    }