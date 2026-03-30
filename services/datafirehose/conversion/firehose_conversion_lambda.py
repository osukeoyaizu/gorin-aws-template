import json
import base64

def lambda_handler(event, context):
    results = []
    records = event["records"]
    for record in records:
        recordId = record["recordId"]
        data = record["data"]
        
        # デコード
        decoded_data = base64.b64decode(data).decode("utf-8")
        print(decoded_data)
        
        # 改行を追加する
        decoded_data = decoded_data + '\n'
        
        # エンコード
        data = base64.b64encode(decoded_data.encode())

        results.append({
            "result":"Ok",
            "recordId":recordId,
            "data":data
        })
        
        
    return {
        "records":results
    }