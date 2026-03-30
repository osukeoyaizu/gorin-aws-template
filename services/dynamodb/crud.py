import json
import datetime
import uuid
import boto3
import os
import math
from decimal import Decimal
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

TABLE = os.environ['TABLE']
PARTITION_KEY = 'id'
SORT_KEY = 'sort_key'

dynamo = boto3.client('dynamodb', region_name='ap-northeast-1')

serializer = TypeSerializer()
deserializer = TypeDeserializer()

# DynamoDBに安全に渡せる形へ再帰変換
def _to_decimal_safe(obj):
    # float を Decimal へ（NaN/Inf を拒否）
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise ValueError("DynamoDBのNumberはNaN/Infinityをサポートしません。値を見直してください。")
        return Decimal(str(obj))
    # すでに Decimal の場合はそのまま
    if isinstance(obj, Decimal):
        return obj
    # 数値（int）はそのまま
    if isinstance(obj, int):
        return obj
    # 文字列/真偽/None はそのまま
    if obj is None or isinstance(obj, (str, bool)):
        return obj
    # dict は各値を再帰処理
    if isinstance(obj, dict):
        return {k: _to_decimal_safe(v) for k, v in obj.items()}
    # list/tuple は各要素を再帰処理（tuple は list にして問題なし）
    if isinstance(obj, (list, tuple)):
        return [_to_decimal_safe(v) for v in obj]
    # その他の型は文字列化する方針もあり得るが、まずはそのままにして失敗させる
    return obj


# 全件取得
def get_data():
    options = {
        'TableName': TABLE,
    }
    response = dynamo.scan(**options)
    data = []
    for item in response['Items']:
        deserized_item = {
            k: deserializer.deserialize(v)
            for k, v in item.items()
        }
        data.append(deserized_item)
    return data


# idに一致したデータを取得
def get_data_byid(id):
    options = {
        'TableName': TABLE,
        'Key': {
            PARTITION_KEY : {'S': id},
            # SORT_KEY: {'S': sort_key}, # ソートキーがある場合(引数追加)
        }
    }
    response = dynamo.get_item(**options)
    
    if response.get('Item'):
        data = {
            k: deserializer.deserialize(v)
            for k, v in response['Item'].items()
        }
        return data
    
    else:
        return None
    

def post_data(data):
    # 入力データを Decimal 安全化
    safe_data = _to_decimal_safe(data)

    item = {
        k: serializer.serialize(v)
        for k, v in safe_data.items()
    }

    options = {
        'TableName': TABLE,
        'Item': item,
    }
    response = dynamo.put_item(**options)
    # 必要に応じて response を返す（Attributes は put_item では通常返らない）
    return safe_data


# データ更新
def put_data(data):
    # 入力データを Decimal 安全化
    safe_data = _to_decimal_safe(data)
    # 更新する項目の設定（値のシリアライズ）
    item = {
        k: serializer.serialize(v)
        for k, v in safe_data.items()
    }

    # キー以外の属性を更新対象にする
    non_key_attrs = [k for k in item.keys() if k != PARTITION_KEY]
    # ソートキーがある場合:
    # non_key_attrs = [k for k in item.keys() if k not in (PARTITION_KEY, SORT_KEY)]

    if not non_key_attrs:
        # 更新対象がない場合は何もしない（必要なら例外にしてもOK）
        return safe_data

    expression_attribute_names = {}

    def to_name_placeholder(attr_name):
        # 可能なら英数字とアンダースコア以外をアンダースコアに変換して安全側に倒す
        safe = ''.join(c if (c.isalnum() or c == '_') else '_' for c in attr_name)
        return f"#k_{safe}"

    # UpdateExpression と ExpressionAttributeValues を構築
    set_clauses = []
    expression_attribute_values = {}

    for key in non_key_attrs:
        name_ph = to_name_placeholder(key)   # 例: "#k_Status"
        val_ph = f":{key}"                   # 例: ":Status"

        expression_attribute_names[name_ph] = key
        expression_attribute_values[val_ph] = item[key]
        set_clauses.append(f"{name_ph} = {val_ph}")

    update_expression = "SET " + ", ".join(set_clauses)

    options = {
        'TableName': TABLE,
        'Key': {
            PARTITION_KEY: {'S': data[PARTITION_KEY]},
            # ソートキーがある場合:
            # SORT_KEY: {'S': data[SORT_KEY]},
        },
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': expression_attribute_values,
        'ExpressionAttributeNames': expression_attribute_names,
        'ReturnValues': 'ALL_NEW'
    }

    response = dynamo.update_item(**options)
    # 必要なら response['Attributes'] を戻す（deserializeして返すなど）
    return safe_data


# データ削除
def delete_data(id):
    options = {
        'TableName': TABLE,
        'Key': {
            PARTITION_KEY: {'S': id},
            # SORT_KEY: {'S': sort_key}, # ソートキーがある場合(引数追加)
        }
    }
    response = dynamo.delete_item(**options)
    return id


# データクエリ
def query_data(
    partition_key: str,
    partition_value: any,
    partition_type: str,
    sort_key: str = None,
    sort_operator: str = None,
    sort_value: any = None,
    sort_value2: any = None,
    sort_type: str = 'N',
    index_name: str = None
):

    def attr_alias(prefix: str) -> str:
        """
        予約語対策用の属性名プレースホルダーを返す。
        prefix は 'pk'（パーティションキー）または 'sk'（ソートキー）。
        """
        return f"#{prefix}"

    def to_av(value: any, dtype: str) -> dict:
        """
        DynamoDB AttributeValue 形式に変換。
        dtype: 'S'|'N'|'BOOL'|'B'|'SS'|'NS'|'BS' などを想定。
        """
        dtype = dtype.upper().strip()
        if dtype == 'N':
            return {dtype: str(value)}
        elif dtype == 'S':
            return {dtype: str(value)}
        elif dtype == 'BOOL':
            return {dtype: bool(value)}
        elif dtype in ('SS', 'NS', 'BS'):
            if value is None:
                return {dtype: []}
            if dtype == 'NS':
                return {dtype: [str(v) for v in value]}
            else:
                return {dtype: list(value)}
        else:
            # その他（B, M, Lなど）を使う場合は必要に応じて拡張
            return {dtype: value}

    # 1) KeyCondition のベース（PK は必須）
    pk_alias = attr_alias('pk')
    expression_names = {pk_alias: partition_key}
    expression_values = {":pkval": to_av(partition_value, partition_type)}
    key_condition = f"{pk_alias} = :pkval"

    params = {
        "TableName": TABLE,
        "KeyConditionExpression": key_condition,
        "ExpressionAttributeNames": expression_names,
        "ExpressionAttributeValues": expression_values,
    }
    if index_name:
        params["IndexName"] = index_name

    # 2) SK 条件や Filter の追加
    if sort_key and sort_operator and sort_value is not None:
        sk_alias = attr_alias('sk')
        expression_names[sk_alias] = sort_key

        op = sort_operator.upper().strip()
        if op == "BETWEEN":
            if sort_value2 is None:
                raise ValueError("BETWEEN を使う場合は sort_value2 が必須です。")
            params["KeyConditionExpression"] += f" AND {sk_alias} BETWEEN :skval1 AND :skval2"
            expression_values[":skval1"] = to_av(sort_value, sort_type)
            expression_values[":skval2"] = to_av(sort_value2, sort_type)

        elif op in ("=", ">=", ">", "<=", "<"):
            params["KeyConditionExpression"] += f" AND {sk_alias} {op} :skval"
            expression_values[":skval"] = to_av(sort_value, sort_type)

        elif op == "BEGINS_WITH":
            params["KeyConditionExpression"] += f" AND begins_with({sk_alias}, :skval)"
            expression_values[":skval"] = to_av(sort_value, sort_type)

        elif op == "CONTAINS":
            # ← ここがポイント：CONTAINS は Filter でのみ使用
            expression_values[":skval"] = to_av(sort_value, sort_type)
            params["FilterExpression"] = f"contains({sk_alias}, :skval)"

        else:
            raise ValueError(f"未対応の sort_operator: {sort_operator}")

    # 3) 実行
    response = dynamo.query(**params)

    items = []
    for item in response.get('Items', []):
        deserized_item = {k: deserializer.deserialize(v) for k, v in item.items()}
        items.append(deserized_item)
    return items


def lambda_handler(event, context):
    # id
    id = str(uuid.uuid4())
    # ttl
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    expiration = int(datetime.datetime.timestamp(expiration))
    # timestamp
    dt = datetime.datetime.now().isoformat()

    # 全件取得
    get_response = get_data()

    # idに一致したデータを取得
    get_byid_response = get_data_byid(id)
    ## ソートキーがある場合
    # get_byid_response = get_data_byid(id, sort_key)


    # データ登録
    post_item = {}
    post_item[PARTITION_KEY] = id
    post_item[SORT_KEY] = 'sort_key'
    post_item['timestamp'] = dt
    post_item['message'] = 'before'
    post_item['expiration'] = expiration
    post_data(post_item)

    # データ更新
    put_item = {}
    put_item[PARTITION_KEY] = id
    put_item[SORT_KEY] = 'sort_key'
    put_item['message'] = 'after'
    put_data(put_item)
    
    # データ削除
    delete_data(id)
    ## ソートキーがある場合
    # delete_data(id, sort_key)

    # データクエリ
    query_item = query_data(
        partition_key='UserId',
        partition_value='USER01',
        partition_type='S',
        sort_key='Point',
        sort_operator='>=',  # HTMLエンティティではなく、正規の演算子文字
        sort_value=100,
        sort_type='N',
        # index_name='UserId-Point-index',  # 必要に応じて指定
    )

    return {
        'statusCode': 200,
        'body': json.dumps(get_response, default=str)
    }