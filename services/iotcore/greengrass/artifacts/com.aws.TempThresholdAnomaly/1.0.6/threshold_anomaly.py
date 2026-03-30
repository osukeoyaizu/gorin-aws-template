import json
import time
import traceback
from concurrent.futures import TimeoutError  # 追加（標準ライブラリ）

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    QOS,
    IoTCoreMessage,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest
)

IOTCORE_TEMP_TOPIC = "sensors/temperature"
IOTCORE_ANOMALY_TOPIC = "alerts/temperature"
THRESHOLD_TEMP = 30.0
QOS_LEVEL = QOS.AT_LEAST_ONCE
TIMEOUT = 10

ipc = awsiot.greengrasscoreipc.connect()

def publish_anomaly(event: dict):
    req = PublishToIoTCoreRequest()
    req.topic_name = IOTCORE_ANOMALY_TOPIC
    req.payload = json.dumps(event).encode("utf-8")
    req.qos = QOS_LEVEL

    op = ipc.new_publish_to_iot_core()
    op.activate(req)
    try:
        op.get_response().result(TIMEOUT)
    except TimeoutError:
        # IoT Core 側で見えているなら、レスポンス待ちの Timeout は致命にしない
        print(f"[WARN] publish timeout (may still be delivered): {IOTCORE_ANOMALY_TOPIC}", flush=True)
    finally:
        # operation は閉じてリソース解放（close() が提供されている）[2](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/greengrasscoreipc.html)
        try:
            op.close().result(2)
        except Exception:
            pass

class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            raw_bytes = event.message.payload
            raw_text = raw_bytes.decode("utf-8", errors="replace")
            print(f"[RAW] {raw_text}", flush=True)

            msg = json.loads(raw_text)

            temp_raw = msg.get("value", msg.get("message"))
            if temp_raw is None:
                raise ValueError("payload must include 'value' or 'message'")

            temp = float(temp_raw)
            ts_raw = msg.get("timestamp", msg.get("ts"))
            ts = int(ts_raw) if ts_raw is not None else int(time.time())

            print(f"[IN] {IOTCORE_TEMP_TOPIC} temp={temp:.2f} ts={ts} msg={msg}", flush=True)

            if temp >= THRESHOLD_TEMP:
                anomaly = {"sensor": "temperature", "value": temp, "threshold": THRESHOLD_TEMP, "ts": ts}
                publish_anomaly(anomaly)
                print(f"[ANOMALY] -> {IOTCORE_ANOMALY_TOPIC} {anomaly}", flush=True)

        except Exception as e:
            print(f"[ERROR] {repr(e)}", flush=True)
            print(traceback.format_exc(), flush=True)

    def on_stream_error(self, error: Exception) -> bool:
        print(f"[STREAM_ERROR] {repr(error)}", flush=True)
        print(traceback.format_exc(), flush=True)
        return True

    def on_stream_closed(self) -> None:
        print("[STREAM_CLOSED]", flush=True)

def main():
    handler = StreamHandler()

    req = SubscribeToIoTCoreRequest()
    req.topic_name = IOTCORE_TEMP_TOPIC
    req.qos = QOS_LEVEL

    op = ipc.new_subscribe_to_iot_core(handler)
    op.activate(req)
    op.get_response().result(TIMEOUT)

    print(f"[READY] subscribed to {IOTCORE_TEMP_TOPIC}", flush=True)

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()