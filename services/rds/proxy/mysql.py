import json
import boto3
import pymysql

region_name = 'ap-northeast-1'
secret_name = "sample-secrets"
table_name = 'analytics'

# シークレット取得
def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    return secret


# データベース接続
def connection_mysql_proxy():
    # シークレット取得
    secret = json.loads(get_secret())
    proxy_host = secret['proxy_host']
    rds_port = secret['port']
    rds_username = secret['username']
    rds_password = secret['password']
    rds_dbname = secret['dbname']

    client = boto3.client('rds', region_name=region_name)
    token = client.generate_db_auth_token(DBHostname=proxy_host, Port=rds_port, DBUsername=rds_username, Region=region_name)
    con = pymysql.connect(host=proxy_host, user=rds_username, password=token, database=rds_dbname, ssl={'ca': 'AmazonRootCA1.pem'})
    return con


# 全データ(リスト型)取得
def get_data_list(con):
    with con.cursor(pymysql.cursors.DictCursor) as cur:
        sql = f"SELECT * FROM {table_name}"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
    return data


def lambda_handler(event, context):
    # データベース接続
    con = connection_mysql_proxy()

    # 全データ(リスト型)取得
    data_list = get_data_list(con)

    return {
        'statusCode': 200,
        'body': json.dumps(data_list, default=str)  # timestampが含まれる場合は json.dumps(data, default=str)
    }