import json
import base64
import gzip
import boto3


def lambda_handler(event, context):
    # CloudWatchLogsからのデータはbase64エンコードされているのでデコード
    decoded_data = base64.b64decode(event['awslogs']['data'])
    # バイナリに圧縮されているため展開
    data = json.loads(gzip.decompress(decoded_data))

    for log in data['logEvents']:
        print(log['message'])

    return {
        'statusCode': 200,
        'body': 'OK'
    }
