
import uuid
from awscrt import mqtt
from awsiot import mqtt_connection_builder, iotshadow

ENDPOINT = "akuwx5saizees-ats.iot.us-east-1.amazonaws.com"
THING_B  = "ThingB"

CA   = "AmazonRootCA1.pem"
CERT = "ThingA.cert.pem"
KEY  = "ThingA.private.key"

#ここの値を変更
MODE = "sport" 

def main():
    mqtt_conn = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT,
        pri_key_filepath=KEY,
        ca_filepath=CA,
        client_id=f"A-{uuid.uuid4()}",
        clean_session=True,
        keep_alive_secs=30
    )
    mqtt_conn.connect().result()
    print("[A] connected")

    shadow = iotshadow.IotShadowClient(mqtt_conn)  # Shadowサービスクライアント[1](https://docs.aws.amazon.com/greengrass/v2/developerguide/interact-with-local-iot-devices.html)[4](https://docs.aws.amazon.com/greengrass/v2/APIReference/Welcome.html)

    # desired を更新（最小）
    state = iotshadow.ShadowState(desired={"mode": MODE})
    req = iotshadow.UpdateShadowRequest(thing_name=THING_B, state=state)
    shadow.publish_update_shadow(req, qos=mqtt.QoS.AT_LEAST_ONCE).result()
    print(f"[A] desired updated: mode={MODE}")

    mqtt_conn.disconnect().result()

if __name__ == "__main__":
    main()
