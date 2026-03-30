import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
# ---- Glue/Spark の初期化 ----
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

import boto3

# ---- コマンドライン引数からパラメータを取得 ----
# ※ 注意：getResolvedOptions を使わずに sys.argv を直接参照しており、順序依存で壊れやすい
REDSHIFT_WORKGROUP = sys.argv[sys.argv.index('--REDSHIFT_WORKGROUP') + 1]
REDSHIFT_ENDPOINT = sys.argv[sys.argv.index('--REDSHIFT_ENDPOINT') + 1]
REDSHIFT_DB_NAME = sys.argv[sys.argv.index('--REDSHIFT_DB_NAME') + 1]
REDSHIFT_SCHEMA_NAME = sys.argv[sys.argv.index('--REDSHIFT_SCHEMA_NAME') + 1]
REDSHIFT_IAM_ROLE = sys.argv[sys.argv.index('--REDSHIFT_IAM_ROLE') + 1]
REGION = sys.argv[sys.argv.index('--REGION') + 1]
OUTPUT_PATH= sys.argv[sys.argv.index('--OUTPUT_PATH') + 1]

# ---- デバッグ用の直書き（本番はコメントアウト推奨）----
# ここで上書きしているため、上の sys.argv 取得は実質使われない点に注意
# REDSHIFT_WORKGROUP = 'workgroup'
# REDSHIFT_ENDPOINT = 'jdbc:redshift://workgroup.157094121738.us-east-1.redshift-serverless.amazonaws.com:5439/dev'
# REDSHIFT_DB_NAME = 'dev'           # JDBC の DB 名（URL と一致させるのが自然）
# REDSHIFT_SCHEMA_NAME = 'public'    # 参照対象のスキーマ
# REDSHIFT_IAM_ROLE = 'arn:aws:iam::157094121738:role/service-role/AmazonRedshift-CommandsAccessRole-20260311T133321'
# REGION = 'us-east-1'
# OUTPUT_PATH = 's3://oyaizu-test/redshift/'  # Glue 一時領域・出力先としても使っている

def get_redshift_data(query):
    # ---- Redshift Serverless の一時クレデンシャルを取得 ----
    redshift_client = boto3.client('redshift-serverless', region_name=REGION)
    response = redshift_client.get_credentials(workgroupName=REDSHIFT_WORKGROUP)

    # 取得できるのは短命の DB ユーザー名・パスワード（有効期限あり）
    db_user = response['dbUser']
    db_password = response['dbPassword']

    # ---- Glue の Redshift コネクションオプション ----
    conn_options = {
        "url": REDSHIFT_ENDPOINT,     # 例: jdbc:redshift://...:5439/dev  （dev がデータベース）
        "user": db_user,              # Serverlessの get_credentials で得た一時ユーザー
        "password": db_password,      # 同パスワード
        "redshiftTmpDir": OUTPUT_PATH,# Glue ジョブが使用するS3一時領域（書込権限必要）
        "aws_iam_role": REDSHIFT_IAM_ROLE,  # S3/Redshift へアクセスするためのロール（信頼関係要）
        "ssl": "true",                # SSL 有効（sslmode=require 相当を使う場合は下記コメント参照）
        # "sslmode": "require"
    }

    # ---- 実行したいクエリ（下で組み立てた SELECT）----
    conn_options["query"] = query

    try:
        # ---- Redshift から DynamicFrame を読み込み ----
        dyf = glueContext.create_dynamic_frame.from_options(
            connection_type="redshift",       # Glue のビルトイン Redshift コネクタ
            connection_options=conn_options,  # 上記オプションをそのまま渡す
            transformation_ctx="redshift_datasource",
        )
        return dyf

    except Exception as e:
        # ---- 失敗時のデバッグ出力（センシティブを出し過ぎないように注意）----
        import traceback
        print("===== Redshift DynamicFrame ERROR =====")
        print("Error message:", str(e))
        print("Stacktrace:")
        traceback.print_exc()

        print("===== Connection options used =====")
        print(conn_options)

        print("===== Redshift credentials =====")
        print("db_user:", db_user)
        # パスワードは出さない（ログに残さない）
        print("TEMP_S3_DIR:", OUTPUT_PATH)
        print("REDSHIFT_ENDPOINT:", REDSHIFT_ENDPOINT)
        print("REDSHIFT_IAM_ROLE:", REDSHIFT_IAM_ROLE)

        raise e

# ---- 取得対象のテーブルを指定したクエリ ----
# ※ Redshift では通常、接続URLの DB（ここでは dev）が選択済みなので、
#    FROM 句は "schema.table" で十分（"dev.public.users" でも動く場合はあるが、基本は "public.users" 推奨）
query = f"select * from {REDSHIFT_DB_NAME}.{REDSHIFT_SCHEMA_NAME}.users"

# ---- Redshift -> DynamicFrame 取得 ----
redshift_dyf = get_redshift_data(query)

# ---- Spark DataFrame に変換 ----
redshift_df = redshift_dyf.toDF()

# ---- pandas に全件収集（※大規模だと OOM の恐れあり）----
pandas_df = redshift_df.toPandas()

import datetime
partition_date = datetime.datetime.now().strftime('%Y-%m-%d')

# ---- pandas で列を追加（partition_date 列に当日日付をセット）----
pandas_df['partition_date'] = partition_date

# ---- pandas -> Spark DataFrame に戻す ----
spark_df = glueContext.spark_session.createDataFrame(pandas_df)

# ---- S3 に CSV 出力 ----
# partitionBy により "partition_date=YYYY-MM-DD/" のディレクトリ配下に書き出される
# ※ coalesce(1) は partitionBy と併用しても「各パーティション1ファイル」を保証しない点に注意
spark_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .partitionBy("partition_date")\
    .csv(OUTPUT_PATH)

# ---- Glue ジョブのコミット ----
job.commit()