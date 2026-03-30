
import json
import time
import uuid
from awscrt import mqtt
from awsiot import mqtt_connection_builder

ENDPOINT = "akuwx5saizees-ats.iot.us-east-1.amazonaws.com"

CA   = "AmazonRootCA1.pem"
CERT = "ThingA.cert.pem"
KEY  = "ThingA.private.key"

REQ_TOPIC  = "rr/request"
RESP_TOPIC = "rr/response"

def main():
    mqtt_conn = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT,
        pri_key_filepath=KEY,
        ca_filepath=CA,
        client_id=f"deviceA-{uuid.uuid4()}",
        clean_session=True,
        keep_alive_secs=30
    )
    mqtt_conn.connect().result()
    print("[A] connected")

    req_id = str(uuid.uuid4())
    done = {"flag": False}

    def on_response(topic, payload, dup, qos, retain, **kwargs):
        msg = json.loads(payload.decode("utf-8"))
        if msg.get("req_id") != req_id:
            return  # 別の応答は無視（最小の相関）
        print("[A] got response:", msg)
        done["flag"] = True

    sub_future, _ = mqtt_conn.subscribe(RESP_TOPIC, mqtt.QoS.AT_LEAST_ONCE, on_response)
    sub_future.result()
    print("[A] subscribed:", RESP_TOPIC)

    # リクエスト送信
    req = {"req_id": req_id, "data": "hello"}
    mqtt_conn.publish(REQ_TOPIC, json.dumps(req), mqtt.QoS.AT_LEAST_ONCE)
    print("[A] sent request req_id=", req_id)

    # 最大10秒待つ（タイムアウト）
    t0 = time.time()
    while not done["flag"] and time.time() - t0 < 10:
        time.sleep(0.1)

    if not done["flag"]:
        print("[A] timeout (no response)")

    mqtt_conn.disconnect().result()

if __name__ == "__main__":
    main()
