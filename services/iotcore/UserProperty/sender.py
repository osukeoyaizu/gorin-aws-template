
import ssl
import json
import time
import base64
import paho.mqtt.client as mqtt

ENDPOINT = "akuwx5saizees-ats.iot.us-east-1.amazonaws.com"
CA   = "AmazonRootCA1.pem"
CERT = "ThingA.cert.pem"
KEY  = "ThingA.private.key"
TOPIC = "demo/userprops"
CLIENT_ID = "sender"

def make_props(ct: str):
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    p = Properties(PacketTypes.PUBLISH)
    p.UserProperty = [("ct", ct)]
    return p

def main():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv5)

    client.tls_set(ca_certs=CA, certfile=CERT, keyfile=KEY)

    client.connect(ENDPOINT, 8883)
    client.loop_start()
    time.sleep(0.3)

    # TEXT
    client.publish(TOPIC, "hello", properties=make_props("text"))
    print("[TX] text")

    # JSON
    client.publish(TOPIC, json.dumps({"temp": 23.4}), properties=make_props("json"))
    print("[TX] json")

    # BINARY（生バイト）
    binaryData = b"1234567890"
    data = base64.b64encode(binaryData)
    client.publish(TOPIC, data, properties=make_props("bin"))
    print("[TX] binary")

    time.sleep(1)
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
