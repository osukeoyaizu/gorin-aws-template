import boto3
import pandas as pd
import io

s3 = boto3.client("s3")

def lambda_handler(event, context):
    # 入力
    bucket = event["bucket"]
    key = event["key"]
    output_bucket = event.get("output_bucket", bucket)
    output_key = event.get("output_key", f"processed/{key}")

    # S3 からファイル取得
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()

    # 拡張子で読み込み処理を分岐
    if key.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(body))

    elif key.endswith(".json"):
        df = pd.read_json(io.BytesIO(body))

    elif key.endswith(".parquet"):
        df = pd.read_parquet(io.BytesIO(body))

    else:
        raise ValueError("Unsupported file type")


    # 保存形式を拡張子で判断
    if output_key.endswith(".csv"):
        out_buffer = io.StringIO()
        df.to_csv(out_buffer, index=False)
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=out_buffer.getvalue().encode("utf-8")
        )

    elif output_key.endswith(".json"):
        out_buffer = io.StringIO()
        df.to_json(out_buffer, orient="records")
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=out_buffer.getvalue().encode("utf-8")
        )

    elif output_key.endswith(".parquet"):
        out_buffer = io.BytesIO()
        df.to_parquet(out_buffer, index=False)
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=out_buffer.getvalue()
        )

    else:
        raise ValueError("Unsupported output file type")

    print(f"Saved processed file to s3://{output_bucket}/{output_key}")

    return {
        "input": f"s3://{bucket}/{key}",
        "output": f"s3://{output_bucket}/{output_key}",
        "rows": len(df),
        "columns": list(df.columns)
    }
