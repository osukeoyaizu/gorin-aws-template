import json
import boto3

def lambda_handler(event, context):

    endpoint_name = "abalone-endpoint"  # あなたのエンドポイント名
    runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")

    # 例: abalone の特徴量8列（※推論時は「特徴量のみ」。ラベル列は含めない）
    payload = "0.5,0.44,0.15,0.08,0.2,0.07,0.09,0.05"

    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Body=payload.encode("utf-8"),
        Accept="text/csv"   # or "application/json"
    )

    result = response["Body"].read().decode("utf-8")
    print("prediction:", result)   # XGBoost は通常 1 行のスコア/ラベルが返る

    return {
        'statusCode': 200,
        'body': json.dumps({"prediction":result}, default=str)
    }
