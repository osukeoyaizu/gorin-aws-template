
import json
import uuid
from awscrt import mqtt
from awsiot import mqtt_connection_builder

ENDPOINT = "akuwx5saizees-ats.iot.us-east-1.amazonaws.com"

CA   = "AmazonRootCA1.pem"
CERT = "ThingB.cert.pem"
KEY  = "ThingB.private.key"

REQ_TOPIC  = "rr/request"
RESP_TOPIC = "rr/response"

def main():
    mqtt_conn = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT,
        pri_key_filepath=KEY,
        ca_filepath=CA,
        client_id=f"deviceB-{uuid.uuid4()}",
        clean_session=True,
        keep_alive_secs=30
    )
    mqtt_conn.connect().result()
    print("[B] connected")

    def on_request(topic, payload, dup, qos, retain, **kwargs):
        msg = json.loads(payload.decode("utf-8"))
        req_id = msg["req_id"]
        data = msg.get("data")

        print(f"[B] recv req_id={req_id} data={data}")

        resp = {"req_id": req_id, "ok": True, "result": f"echo:{data}"}
        mqtt_conn.publish(RESP_TOPIC, json.dumps(resp), mqtt.QoS.AT_LEAST_ONCE)
        print(f"[B] sent response req_id={req_id}")

    # subscribe は (future, topic) のタプルが返る実装の場合があるため future を取り出す
    sub_future, _ = mqtt_conn.subscribe(REQ_TOPIC, mqtt.QoS.AT_LEAST_ONCE, on_request)
    sub_future.result()
    print("[B] subscribed:", REQ_TOPIC)

    # 常駐（受信はSDK内部の非同期I/Oで進む）[2](https://docs.aws.amazon.com/greengrass/v2/developerguide/interact-with-local-iot-devices.html)
    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
