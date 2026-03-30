import json
import boto3

s3 = boto3.client('s3')

# s3バケットからファイルを取得する
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
    prefix = ''
    
    # s3バケットからファイルを取得する
    objects = list_objects_v2(bucket, prefix)

    return {
        'statusCode': 200,
        'body': 'OK'
    } 