
import ssl
import json
import base64
import paho.mqtt.client as mqtt

ENDPOINT = "akuwx5saizees-ats.iot.us-east-1.amazonaws.com"
CA   = "AmazonRootCA1.pem"
CERT = "ThingB.cert.pem"
KEY  = "ThingB.private.key"
TOPIC = "demo/userprops"
CLIENT_ID = "receiver"

def on_connect(c, u, f, rc, p=None):
    c.subscribe(TOPIC)
    print("[RX] connected, subscribed:", TOPIC)

def on_message(c, u, msg):
    props = dict(msg.properties.UserProperty or []) if msg.properties else {}
    print("ユーザープロパティ", props)
    ct = props.get("ct")

    if ct == "bin":
        print(f"[RX] BINARY:", base64.b64decode(msg.payload))
        
    elif ct == "json":
        print("[RX] JSON:", json.loads(msg.payload.decode()))
        
    elif ct == "text":
        print("[RX] TEXT:", msg.payload.decode())


def main():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set(ca_certs=CA, certfile=CERT, keyfile=KEY)
    client.connect(ENDPOINT, 8883)

    client.loop_forever()

if __name__ == "__main__":
    main()
