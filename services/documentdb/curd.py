import json
import os
import boto3
import pymongo
from bson import ObjectId

REGION_NAME = os.environ['REGION_NAME']
SECRETS_NAME = os.environ['SECRETS_NAME']
DB_NAME = os.environ['DB_NAME']
COLLECTION_NAME = os.environ['COLLECTION_NAME']

# -------------------------
# Secret取得
# -------------------------
def get_secret():
    client = boto3.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )
    response = client.get_secret_value(SecretId=SECRETS_NAME)
    return json.loads(response['SecretString'])


# -------------------------
# DocumentDB 接続
# -------------------------
def get_documentdb_client():
    secret = get_secret()

    uri = (
        f"mongodb://{secret['username']}:{secret['password']}"
        f"@{secret['host']}:{secret['port']}"
        f"/?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
    )

    client = pymongo.MongoClient(uri)
    return client


# -------------------------
# 全件取得
# -------------------------
def get_all(col):
    data = list(col.find({}))
    return json_safe(data)


# -------------------------
# _id 指定取得
# -------------------------
def get_by_id(col, id):
    data = col.find_one({"_id": ObjectId(id)})
    return json_safe(data)


# -------------------------
# 登録
# -------------------------
def insert_data(col, document):
    result = col.insert_one(document)
    return str(result.inserted_id)


# -------------------------
# 更新
# -------------------------
def update_data(col, id, document):
    col.update_one(
        {"_id": ObjectId(id)},
        {"$set": document}
    )


# -------------------------
# 削除
# -------------------------
def delete_data(col, id):
    col.delete_one({"_id": ObjectId(id)})


# -------------------------
# ObjectId を JSON 化
# -------------------------
def json_safe(data):
    if isinstance(data, list):
        for d in data:
            d["_id"] = str(d["_id"])
        return data
    if isinstance(data, dict):
        data["_id"] = str(data["_id"])
        return data
    return data


# -------------------------
# Lambda handler
# -------------------------
def lambda_handler(event, context):
    client = get_documentdb_client()
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]

    # Create
    new_id = insert_data(col, {
        "text": "sample",
        "status": "active"
    })

    # Read（全件）
    all_data = get_all(col)

    # Read（ID指定）
    one_data = get_by_id(col, new_id)

    # Update
    update_data(col, new_id, {
        "text": "updated sample"
    })

    # Delete
    delete_data(col, new_id)

    client.close()

    return {
        "statusCode": 200,
        "body": json.dumps({"all": all_data}, ensure_ascii=False)
    }