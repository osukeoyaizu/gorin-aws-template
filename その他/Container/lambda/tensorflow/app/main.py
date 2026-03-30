import base64
import json
import tensorflow as tf
import urllib.request
import boto3

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

model = tf.keras.models.load_model('./model.h5', compile=False)

def load_image_from_bytes(img_bytes):
    img = tf.io.decode_image(img_bytes, channels=3, expand_animations=False)
    img = tf.image.resize(img, (224, 224))
    img = tf.cast(img, tf.float32)
    img = tf.expand_dims(img, axis=0)
    return preprocess_input(img)

def load_image_from_url(url):
    response = urllib.request.urlopen(url)
    img_bytes = response.read()
    return load_image_from_bytes(img_bytes)

def load_image_from_s3(bucket, key):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    img_bytes = obj["Body"].read()
    return load_image_from_bytes(img_bytes)

def handler(event, context):
    body = event.get("body", event)

    if type(body) is str:
        body = json.loads(body)

    img_tensor = None

    if "image" in body:
        b64 = body["image"]
        if "base64," in b64:
            b64 = b64.split("base64,", 1)[1]
        img_bytes = base64.b64decode(b64)
        img_tensor = load_image_from_bytes(img_bytes)

    elif "image_url" in body:
        img_tensor = load_image_from_url(body["image_url"])

    elif "s3_bucket" in body and "s3_key" in body:
        img_tensor = load_image_from_s3(body["s3_bucket"], body["s3_key"])

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "image / image_url / s3_bucket+s3_key のいずれかが必要です"})
        }

    pred = model(img_tensor, training=False).numpy()
    result = decode_predictions(pred, top=5)[0]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps({
            "predictions": [{"label": r[1], "score": float(r[2])} for r in result]
        }, ensure_ascii=False)
    }
