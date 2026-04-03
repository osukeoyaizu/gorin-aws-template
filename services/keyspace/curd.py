import json
import uuid
import datetime

from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra import ConsistencyLevel
from cassandra.policies import RoundRobinPolicy
from cassandra.query import dict_factory
from cassandra_sigv4.auth import SigV4AuthProvider

from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED

# =====================================================
# 設定
# =====================================================
KEYSPACE = "gorin"
TABLE = "table1"
REGION = "us-east-1"

PARTITION_KEY = "id"

# ===== ソートキーを使う場合 =====
# SORT_KEY = "sort_key"
# USE_SORT_KEY = True

# ===== ソートキーなし =====
USE_SORT_KEY = False

# =====================================================
# TLS / 認証
# =====================================================
ssl_context = SSLContext(PROTOCOL_TLSv1_2)
ssl_context.verify_mode = CERT_REQUIRED
ssl_context.load_default_certs()

auth_provider = SigV4AuthProvider(region_name=REGION)

# =====================================================
# Execution Profile（必須）
# =====================================================
profile = ExecutionProfile(
    consistency_level=ConsistencyLevel.LOCAL_QUORUM,
    load_balancing_policy=RoundRobinPolicy(),
    row_factory=dict_factory,
)

cluster = Cluster(
    [f"cassandra.{REGION}.amazonaws.com"],
    port=9142,
    ssl_context=ssl_context,
    auth_provider=auth_provider,
    protocol_version=4,
    execution_profiles={EXEC_PROFILE_DEFAULT: profile},
)

session = cluster.connect(KEYSPACE)

# =====================================================
# 全件取得（PK単位）
# =====================================================
def get_all_by_partition(partition_value: str):
    cql = f"""
    SELECT * FROM {TABLE}
    WHERE {PARTITION_KEY} = %s
    """
    return list(session.execute(cql, (partition_value,)))

# =====================================================
# 1件取得
# =====================================================
def get_data_byid(id: str, sort_key=None):
    if USE_SORT_KEY:
        cql = f"""
        SELECT * FROM {TABLE}
        WHERE {PARTITION_KEY} = %s
          AND {SORT_KEY} = %s
        """
        return session.execute(cql, (id, sort_key)).one()
    else:
        cql = f"""
        SELECT * FROM {TABLE}
        WHERE {PARTITION_KEY} = %s
        """
        return session.execute(cql, (id,)).one()

# =====================================================
# 登録 / 更新（UPSERT）
# =====================================================
def post_data(data: dict):
    insert_data = data.copy()
    if not USE_SORT_KEY:
        insert_data.pop("sort_key", None)

    columns = ", ".join(insert_data.keys())
    placeholders = ", ".join(["%s"] * len(insert_data))
    values = tuple(insert_data.values())

    cql = f"""
    INSERT INTO {TABLE} ({columns})
    VALUES ({placeholders})
    """
    session.execute(cql, values)
    return insert_data

# =====================================================
# 部分更新
# =====================================================
def put_data(data: dict):
    update_fields = []
    values = []

    for k, v in data.items():
        if k != PARTITION_KEY and (not USE_SORT_KEY or k != SORT_KEY):
            update_fields.append(f"{k} = %s")
            values.append(v)

    if not update_fields:
        return data

    if USE_SORT_KEY:
        cql = f"""
        UPDATE {TABLE}
        SET {", ".join(update_fields)}
        WHERE {PARTITION_KEY} = %s AND {SORT_KEY} = %s
        """
        values.extend([data[PARTITION_KEY], data[SORT_KEY]])
    else:
        cql = f"""
        UPDATE {TABLE}
        SET {", ".join(update_fields)}
        WHERE {PARTITION_KEY} = %s
        """
        values.append(data[PARTITION_KEY])

    session.execute(cql, tuple(values))
    return data

# =====================================================
# 削除
# =====================================================
def delete_data(id: str, sort_key=None):
    if USE_SORT_KEY:
        session.execute(
            f"DELETE FROM {TABLE} WHERE {PARTITION_KEY}=%s AND {SORT_KEY}=%s",
            (id, sort_key),
        )
    else:
        session.execute(
            f"DELETE FROM {TABLE} WHERE {PARTITION_KEY}=%s",
            (id,),
        )

# =====================================================
# Lambda handler
# =====================================================
def lambda_handler(event, context):
    id = 1
    # sort_key = "sample"
    now = datetime.datetime.now().isoformat()

    post_item = {}
    post_item[PARTITION_KEY] = id
    # post_item[SORT_KEY] = sort_key
    post_item["message"] = "before"
    post_item["timestamp"] = now
    post_item["expiration"] = 30

    # INSERT（= 更新含む）
    post_data(post_item)

    # 全件取得（このPK配下）
    items = get_all_by_partition(id)

    # 一件取得
    item = get_data_byid(id)
    # item = get_data_byid(id, sort_key)

    return {
        "statusCode": 200,
        "body": json.dumps(items, ensure_ascii=False),
    }