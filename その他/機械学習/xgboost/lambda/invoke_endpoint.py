# lambda_function.py
import os
import json
import boto3

ENDPOINT_NAME = os.environ.get("SM_ENDPOINT_NAME", "abalone-xgb-dev-endpoint")
runtime = boto3.client("sagemaker-runtime")
# ---------------------------------------------------------------------------

def lambda_handler(event, context):
    """
    Abalone 例）学習時の f0〜f7 と同じ順序で 8 特徴量を構成してください。
      f0: SexEncoded(M=0,F=1,I=2), f1: Length, f2: Diameter, f3: Height,
      f4: Whole weight, f5: Shucked weight, f6: Viscera weight, f7: Shell weight
    """
    # ★ここを実際の入力に合わせて組み立てる（例として固定値）
    instance = [0.5, 0.44, 0.15, 0.08, 0.2, 0.07, 0.09, 0.05]

    # 推論サーバは JSON を想定（{"instances":[[...]]}）
    payload = {"instances": [instance]}
    print(payload)
    body_bytes = json.dumps(payload).encode("utf-8")

    resp = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=body_bytes,
    )
    # サーバの戻りは {"predictions":[...]} の JSON
    result_str = resp["Body"].read().decode("utf-8")
    result_obj = json.loads(result_str)
    pred = float(result_obj["predictions"][0])

    return {
        "statusCode": 200,
        "body": json.dumps({"score": pred}),
    }