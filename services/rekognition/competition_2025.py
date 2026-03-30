import json
import os
import boto3
import urllib.request
import requests
import io
import datetime
import pprint

bucket_name = os.environ['BUCKET']
token_url = os.environ['TOKEN_URL']
cats_table = os.environ['CATS_TABLE']
dogs_table = os.environ['DOGS_TABLE']
unknown_table = os.environ['UNKNOWN_TABLE']
sqs_queue_url = os.environ['SQS_QUEUE_URL']
api_url = os.environ['API_URL']
region_name = os.environ['REGION_NAME']

s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb', region_name=region_name)
rekognition_client = boto3.client('rekognition')
sqs_client = boto3.client('sqs', region_name=region_name)

# ttl作成
expiration = datetime.datetime.now() + datetime.timedelta(days=90)
ttl = int(datetime.datetime.timestamp(expiration))

# 開始時間
start_time = time.time()

# # 90日を秒に変換
# ttl_seconds = 90 * 24 * 60 * 60  # 90日を秒に変換
# current_time = int(time.time())  # 現在のUNIXタイムスタンプを取得
# ttl_timestamp = current_time + ttl_seconds  # TTLのタイムスタンプを計算


def get_tokens():
    # txtファイルのダウンロード
    response = requests.get(token_url)
    tokens = response.text.splitlines()
    return tokens

    # # txtファイル取得
    # com=urllib.request.urlopen(token_url)
    # un=com.read().decode()
    # # 改行毎にリストに追加する
    # tokens = un.split()
    # return tokens



    

def lambda_handler(event, context):

    # トークンテキスト取得メソッド
    tokens = get_tokens()

    table = {}
    count = 0

    for token in tokens:
        count = count + 1
        
        try:
            # urlにアクセスして画像アクセスurl取得
            response = requests.get(f'{api_url}/?token={token}')
            response_data = response.json()
            
            image_url = response_data['url']

            # urlにアクセスして画像取得
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            # 画像データをバイト型で取得
            image_bytes = image_response.content

            image_content = io.BytesIO(image_bytes)

            rekognition_response = rekognition_client.detect_labels(
            Image={
                'Bytes': image_bytes
                }
            )

            # response['Labels']をlabelに格納し、label['Name]に'Cat'か'Dog'があったらlabel['Name']の値をanimal_typesに格納する
            animal_types = [label['Name'] for label in rekognition_response['Labels'] if 'Cat' in label['Name'] or 'Dog' in label['Name']]
            # response['Labels']をlabelに格納し、label['Name]に'Cat'か'Dog'があったらlabel['Confidence']の値をconfidence_listに格納する
            confidence_list = [label['Confidence'] for label in rekognition_response['Labels'] if 'Cat' in label['Name'] or 'Dog' in label['Name']]

            if animal_types:
                animal_ytpe = animal_types[0]
                confidence = confidence_list[0]

                folder_name = ""
                tableName = ""

                # 保存先(s3フォルダ,DynamoDBテーブル)の決定
                if animal_ytpe.lower() == 'cat' and confidence >= 80:
                    folder_name = 'cats/'
                    tableName = cats_table
                    
                elif animal_ytpe.lower() == 'dog' and confidence >= 80:
                    folder_name = 'dogs/'
                    tableName = dogs_table
                else:
                    folder_name = 'unknown/'
                    tableName = unknown_table
                
                
                # s3に保存するデータ
                body = image_content

                # s3に画像を保存
                key_name = f'{folder_name}{os.path.basename(image_url)}'
                s3_client.put_object(Bucket=bucket_name,Key=key_name, Body=body)

                # DynamoDBテーブルに保存するデータ
                item = {
                    'Passcode': {'S':token},
                    'URL': {'S':image_url},
                    'Confidence': {'N':str(confidence)},
                    'ttl': {'N':str(ttl)}
                }

                # DynamoDBに結果を登録
                dynamodb_client.put_item(TableName=tableName, Item=item)

        except Exception as e:
            # エラーが発生した場合、その行をSQSに送信
            error_message = f"Failed to process line '{token}': {str(e)}"
            sqs_client.send_message(
                QueueUrl=sqs_queue_url,
                MessageBody=error_message
            )
            print(error_message)  # エラーメッセージを出力
    # 終了時間
    end_time = time.time()
    # 合計時間
    time_diff = end_time - start_time
    print(time_diff)
    return {
        'statusCode': 200,
        'body': 'OK'
    }
