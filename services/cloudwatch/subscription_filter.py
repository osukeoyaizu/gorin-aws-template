import json
import base64
import gzip

#サブスクリプションフィルタで検知した文字列を取得
def decode_function(event):
    decoded_message = base64.b64decode(event['awslogs']['data'])
    decompressed_data = gzip.decompress(decoded_message)
    json_data = json.loads(decompressed_data)
    log_message = json_data['logEvents'][0]['message']
    
    return log_message
    
def lambda_handler(event, context):
    log_message = decode_function(event)
    print(log_message)

