import pika
import json
import ssl

BROKER_HOST = 'b-xxxxxyyyyy.mq.<region>.on.aws'
BROKER_PORT = 5671
USERNAME = 'admin'
PASSWORD = '<password>'
QUEUE_NAME = 'orders'

# 認証情報
credentials = pika.PlainCredentials(USERNAME, PASSWORD)

# ✅ SSL/TLS コンテキスト（必須）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# 接続パラメータ
parameters = pika.ConnectionParameters(
    host=BROKER_HOST,
    port=BROKER_PORT,
    credentials=credentials,
    ssl_options=pika.SSLOptions(ssl_context)
)

# 接続とチャネルの作成
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# キューの宣言（存在しなければ作成）
channel.queue_declare(queue=QUEUE_NAME, durable=True)

print(f"Waiting for messages from queue: {QUEUE_NAME}")
print("To exit press CTRL+C")

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(
        f"Received: Order ID={order['order_id']}, "
        f"Product={order['product']}, "
        f"Quantity={order['quantity']}, "
        f"Price={order['price']}"
    )
    print("-" * 50)

    # ACK（重要）
    ch.basic_ack(delivery_tag=method.delivery_tag)

# コンシューマー設定
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nConsumer stopped")
    channel.stop_consuming()
finally:
    connection.close()