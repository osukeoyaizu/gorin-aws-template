import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
# Spark/Glue の初期化
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

import boto3

# ---- コマンドライン引数からパラメータを取得 ----
# ※ getResolvedOptions を使わずに sys.argv を直接参照している（動くが壊れやすい）
RDS_HOST = sys.argv[sys.argv.index('--RDS_HOST') + 1]
RDS_USER = sys.argv[sys.argv.index('--RDS_USER') + 1]
RDS_PORT = sys.argv[sys.argv.index('--RDS_PORT') + 1]
RDS_DB = sys.argv[sys.argv.index('--RDS_DB') + 1]
REGION = sys.argv[sys.argv.index('--REGION') + 1]
OUTPUT_PATH= sys.argv[sys.argv.index('--OUTPUT_PATH') + 1]

# # デバッグ用の直書き例（本番ではコメントアウトのままでOK）
# RDS_HOST = 'test.c3jn0kosadjl.us-east-1.rds.amazonaws.com'
# RDS_USER = 'iam_db_user'
# RDS_PORT = '3306'
# RDS_DB = 'gorin'
# REGION = 'us-east-1'
# OUTPUT_PATH = 's3://oyaizu-test/rds/'

def get_rds_table(query):
    # 認証トークンを生成
    client = boto3.client('rds', region_name=REGION)
    token = client.generate_db_auth_token(
        DBHostname=RDS_HOST,
        Port=RDS_PORT,
        DBUsername=RDS_USER,
        Region=REGION
    )

    jdbc_url = f"jdbc:mysql://{RDS_HOST}:{RDS_PORT}/{RDS_DB}?sslMode=REQUIRED&useSSL=true"

    try:
        dyf = glueContext.create_dynamic_frame.from_options(
            connection_type="mysql",
            connection_options={
                "url": jdbc_url,
                "user": RDS_USER,
                "password": token,
                "dbtable": RDS_DB,
                "sampleQuery": query
            }
        )
    except Exception as e:
        import traceback
        print("===== RDS DynamicFrame ERROR =====")
        print("Error message:", str(e))
        print("Stacktrace:")
        traceback.print_exc()

        print("===== RDS Connection Info =====")
        print("RDS_HOST:", RDS_HOST)
        print("RDS_USER:", RDS_USER)
        print("JDBC URL:", jdbc_url)

        print("===== Likely Causes =====")
        print("1. RDS のセキュリティグループが Glue の SG を許可していない")
        print("2. admin ユーザーに SELECT 権限がない")
        print("3. IAM 認証が RDS 側で有効化されていない")
        print("4. Glue の VPC 設定が RDS と同じでない")

        raise e

    return dyf

# ---- 実行したい SQL（RDS/MySQL 側にあるテーブル 'sample' から全件取得）----
query = "select * from sample"

# ---- RDS -> Glue DynamicFrame 取得 ----
rds_dyf = get_rds_table(query)

# ---- Spark DataFrame へ変換 ----
rds_df = rds_dyf.toDF()

# ---- （非推奨寄り）一度 pandas に全件集約 ----
# データ量が多いとドライバーに載り切らず OOM の原因になる
pandas_df = rds_df.toPandas()

import datetime
partition_date = datetime.datetime.now().strftime('%Y-%m-%d')

# ---- pandas で列を追加（列に当日の日付を入れる）----
pandas_df['partition_date'] = partition_date

# ---- pandas -> Spark DataFrame に戻す ----
spark_df = glueContext.spark_session.createDataFrame(pandas_df)

# ---- S3 に CSV 出力 ----
# partitionBy でパーティションディレクトリ（partition_date=YYYY-MM-DD/）に分けて書き出す
# coalesce(1) は 'partitionBy' が入ると意図通り「各パーティション1ファイル」とは限らない点に注意
spark_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .partitionBy("partition_date")\
    .csv(OUTPUT_PATH)

# ---- Glue Job のコミット ----
job.commit()