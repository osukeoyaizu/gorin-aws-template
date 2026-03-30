import json
import boto3
import pandas as pd
import io

s3 = boto3.client('s3')

# s3バケットからファイル一覧を取得する（あなたの関数）
def list_objects_v2(bucket, prefix):
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    object_key_list = []
    for item in response['Contents']:
        # フォルダ除外
        if item['Key'][-1] == '/':
            continue
        object_key_list.append(item['Key'])
    return object_key_list

def lambda_handler(event, context):
    bucket = 'sample'
    prefix = 'data/'

    # フォルダ内のファイル一覧取得
    objects = list_objects_v2(bucket, prefix)

    dfs = []

    for key in objects:
        # S3 から CSV を取得
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read()

        # pandas DataFrame に変換
        df = pd.read_csv(io.BytesIO(body))
        df["source_file"] = key  # 任意：どのファイルか記録
        dfs.append(df)

    # 全 CSV を結合
    merged_df = pd.concat(dfs, ignore_index=True)
    print(merged_df)

    return {
        'statusCode': 200,
        'rows': len(merged_df),
        'columns': list(merged_df.columns),
        'files_loaded': len(dfs)
    }
