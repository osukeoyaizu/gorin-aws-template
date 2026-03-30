import json
import base64
import re
import datetime

def lambda_handler(event, context):
    print(json.dumps(event))
    results = []

    for record in event["records"]:
        record_id = record["recordId"]
        encoded_data = record["data"]

        # デコード
        decoded_str = base64.b64decode(encoded_data).decode("utf-8")

        # ログからタイムスタンプ抽出
        match = re.search(r'\[(.*?)\]', decoded_str)
        if match:
            timestamp_str = match.group(1)
            try:
                log_datetime = datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z').isoformat()
            except Exception as e:
                log_datetime = None
        else:
            log_datetime = None

        # JSON形式に変換
        transformed = {
            "log": decoded_str,
            "timestamp": log_datetime
        }

        json_str = json.dumps(transformed) + "\n"
        encoded_result = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        results.append({
            "recordId": record_id,
            "result": "Ok",
            "data": encoded_result
        })

    return {
        "records": results
    }
