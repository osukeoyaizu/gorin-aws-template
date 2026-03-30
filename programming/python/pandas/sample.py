import json
import boto3
import base64
import io
import pandas as pd
import datetime
import uuid

table_name = 'gorin'
s3 = boto3.client('s3', region_name='ap-northeast-1')

# バケットのオブジェクトのリスト取得
def list_objects(bucket):
    response = s3.list_objects_v2(
        Bucket=bucket
    )
    return response


# オブジェクトを削除
def delete_object(bucket, key):
    response = s3.delete_object(
        Bucket=bucket,
        Key=key
    )
    return response


def lambda_handler(event, context):
    bucket = 'lab3-s3-0320'
    response = list_objects(bucket)
    key_list = []
    df1 = pd.DataFrame(index=None)
    for item in response['Contents']:
        key_list.append(item['Key'])
        s3_object = s3.get_object(Bucket=bucket, Key=item['Key'])
        data = s3_object['Body'].read()
        content = data.decode()
        df2 = pd.read_csv(io.StringIO(content))
        df1 = pd.concat([df1, df2])
    
    # カラム名を変更
    df1.rename(columns=({'time': 'datetime'}))

    # 数値変換(変換できないものはNaN)
    df1['number'] = pd.to_numeric(df1['number'], errors='coerce')
    
    # unixtime → datetime
    df1['datetime'] = pd.to_datetime(df1['datetime'], unit='s')

    # datetime → string
    df1['datetime'] = df1['datetime'].astype(str)
    # datetime → string(フォーマット指定)
    df1['datetime_str'] = df1['datetime'].dt.strftime('%Y-%m-%d') 


    # string → datetime
    df1['datetime'] = pd.to_datetime(df1['datetime_str'],format='%d/%b/%Y:%H:%M:%S%z')


    # 数値の欠損値を平均値で補完
    df1.fillna(df1.mean(numeric_only=True))

    # 文字列型に変換し、プレフィックス追加
    df1['temperature'] = 'ex. ' + df1['temperature'].astype(str)
    df1['humidity'] = 'ex. ' + df1['humidity'].astype(str)

    # 条件一致したデータを抽出
    df1.loc[df1['datetime'] >= datetime.datetime.now()]

    # 条件一致したデータに特定の値の列を追加
    df1.loc[df1['user_agent'].str.contains('iPhone|Android'), 'device_type'] = 'Moble'

    # 条件一致したデータを抽出
    filter_date = datetime.datetime.now().strftime('%Y-%m-%d')
    yaer, month, day = filter_date.split('-')
    pandas_df = pandas_df.loc[
        (pandas_df['partition_0'].astype(str) == yaer) &
        (pandas_df['partition_1'].astype(str) == month) &
        (pandas_df['partition_2'].astype(str) == day)
    ]

    # 特定の文字(文字列)を含んだ行を削除
    df1.loc[~df1['user_agent'].str.contains('Mac')]

    # 値を置換
    df1['timestamp_utc'].str.replace('[', '').str.replace(']','')

    # null値を置換
    df1.loc[df1['device_type'].isnull(), 'device_type'] = 'Desktop'
    
    # 辞書型に変換
    dict_data = df1.to_dict(orient='records')

    # カラム順変換
    df1 = df1.reindex(columns=[
        "column1", "column2", "column3"
    ])

    # カラム名変換
    df1.rename(columns=({'都道府県': '都道府県名'}))
    
    # UUID列追加
    df1['uuid'] = [str(uuid.uuid4()) for _ in range(len(df1))]

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
