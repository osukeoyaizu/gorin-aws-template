import pika
import json
import time
import ssl

BROKER_HOST = 'b-xxxxxyyyyy.mq.<region>.on.aws'
BROKER_PORT = 5671
USERNAME = 'admin'
PASSWORD = '<password>'
QUEUE_NAME = 'orders'

# 認証情報
credentials = pika.PlainCredentials(USERNAME, PASSWORD)

# SSL コンテキスト作成（Amazon MQ 用）
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

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# キュー作成（なければ作成）
channel.queue_declare(queue=QUEUE_NAME, durable=True)

orders = [
    {'order_id': 1, 'product': 'Laptop', 'quantity': 1, 'price': 89900},
    {'order_id': 2, 'product': 'Mouse', 'quantity': 2, 'price': 2500},
]

for order in orders:
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(order),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Sent: {order}")
    time.sleep(1)

connection.close()
print("All messages sent successfully")