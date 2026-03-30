import json
import boto3

s3 = boto3.client('s3')

# s3バケットからlambdaにファイルダウンロード
def download_file(bucket, key, local_file_path):
    s3.download_file(bucket, key, local_file_path)

# ファイルの内容を読む
def read_file(local_file_path):
    with open(local_file_path) as f:
        data = f.read()
        print(data)
    return data


def lambda_handler(event, context):
    bucket = 'lab2-s3'
    key = 'test/test.txt'
    local_file_path = '/tmp/oyaizu.txt' # /tmp以下のファイルしか変更できない、階層構造にできない


    # s3バケットからlambdaにファイルダウンロード
    download_file(bucket, key, local_file_path)

    # ファイルの内容を読む
    data = read_file()
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }
