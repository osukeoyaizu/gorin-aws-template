import json
import math
import random
import time
import uuid
import datetime
import boto3

STREAM_NAME = "oyaizu"
REGION = "us-east-1"
DEVICE_IDS = [f"device_{i}" for i in range(1, 101)]

# ★ 異常発生確率（例：1%）
ANOMALY_PROB = 0.001


def generate_value(t: float, anomaly_prob: float = ANOMALY_PROB) -> float:
    """
    通常は時間ベースのサイン波、指定した確率で val=17（異常値）を発生させる
    ※ t は time.time() の秒
    """
    rad = (t % 60) / 60 * (2 * math.pi)  # 1分周期
    normal_value = math.sin(rad) * 10 + 10  # 0〜20付近を往復

    # ★ 確率的に異常値（17）を出す
    if random.random() < anomaly_prob:
        return -17.0

    return normal_value

def build_record(anomaly_prob: float = ANOMALY_PROB):
    """Kinesis に送る1レコードを構築"""
    device_id = random.choice(DEVICE_IDS)
    ts = int(datetime.datetime.now().timestamp())
    t = time.time()
    is_active = random.choice([True, False])
    return {
        "device_id": device_id,
        "timestamp": ts,
        "value": generate_value(t, anomaly_prob=anomaly_prob),
        "is_active": is_active,
        "event_id": f"{device_id}-{int(t * 1000)}-{uuid.uuid4().hex[:6]}"
    }

def generate(hz=100, anomaly_prob: float = ANOMALY_PROB):
    """Kinesis に連続送信（デフォルト100Hz）"""
    kinesis = boto3.client("kinesis", region_name=REGION)
    period = 1.0 / hz
    while True:
        record = build_record(anomaly_prob=anomaly_prob)
        kinesis.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(record).encode("utf-8"),
            PartitionKey=record["device_id"]
        )
        time.sleep(period)
        print(record)

if __name__ == "__main__":
    # 例：10% の確率で val=17 を出したい場合
    # generate(hz=100, anomaly_prob=0.10)
    generate(hz=100, anomaly_prob=ANOMALY_PROB)