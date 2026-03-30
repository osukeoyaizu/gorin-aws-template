import json
import boto3
import psycopg2, psycopg2.extras


region_name = 'us-east-1'
secret_name = "postgresql"
table_name = 'users'

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
def connection_postgresql_iam_auth():
    # シークレット取得
    secret = json.loads(get_secret())
    rds_host = secret['host']
    rds_port = secret['port']
    rds_username = secret['username']
    rds_dbname = secret['dbname']

    client = boto3.client('rds', region_name=region_name)
    token = client.generate_db_auth_token(DBHostname=rds_host, Port=rds_port, DBUsername=rds_username, Region=region_name)
    print(token)
    con = psycopg2.connect(host=rds_host, user=rds_username, password=token, dbname=rds_dbname, sslrootcert='us-east-1-bundle.pem', sslmode='verify-ca')
    return con


# 全データ(リスト型)取得
def get_data_list(con):
    with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        sql = f"SELECT * FROM {table_name}"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
    return data


def lambda_handler(event, context):
    # データベース接続
    con = connection_postgresql_iam_auth()

    # 全データ(リスト型)取得
    data_list = get_data_list(con)

    return {
        'statusCode': 200,
        'body': json.dumps(data_list, default=str)  # timestampが含まれる場合は json.dumps(data, default=str)
    }