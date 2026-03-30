import base64
import json
import datetime
import boto3
import os

timestream = boto3.client('timestream-write')

DATABASE_NAME = os.environ['DATABASE_NAME']
TABLE_NAME = os.environ['TABLE_NAME']


def make_record(unixtime, device_id, temperature, humidity):
    record ={
                "Dimensions": [
                    {"Name": "deviceId", "Value": device_id, "DimensionValueType": "VARCHAR"},
                ],
                "MeasureValueType": "MULTI",  # マルチメジャーレコード
                "MeasureName": "sensorData",
                "Time": str(int(unixtime)),
                "TimeUnit": "MILLISECONDS",
                "MeasureValues": [
                    {
                        "Name": "temperature",
                        "Value": str(temperature),
                        "Type": "DOUBLE",
                    },
                    {
                        "Name": "humidity",
                        "Value": str(humidity),
                        "Type": "DOUBLE",
                    },
                ],
            }
    return record

def write_records(database_name, table_name, records):
    response = timestream.write_records(
        DatabaseName=database_name,
        TableName=table_name,
        Records=records,
    )

# Kinesis Datastreamトリガーで取得したデータをTimestreamに保存
def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        print(data)
        data = json.loads(data)
        device_id = data['DEVICE_Id']
        timestamp = data['TIMESTAMP']
        temperature = data['TEMPERATURE']
        humidity = data['HUMIDITY']

        # isoformat形式のデータをunixtime形式に変換する
        unixtime = datetime.datetime.fromisoformat(timestamp).timestamp() * 1000
        timestream_records = []
        # 保存するレコード作成
        timestream_record = make_record(unixtime, device_id, temperature, humidity)
        timestream_records.append(timestream_record)

        # 保存処理
        write_records(DATABASE_NAME, TABLE_NAME, timestream_records)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



# Timestreamテーブルは「デフォルトパーティショニング」を選択する