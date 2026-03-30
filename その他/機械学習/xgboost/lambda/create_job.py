# lambda_training.py
import boto3
import os
import json
import pandas as pd
from datetime import datetime, timezone

s3 = boto3.client("s3")
sagemaker = boto3.client("sagemaker")
lambda_client = boto3.client("lambda")

def _now_id():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

def _split_train_val(df, ratio=0.8, seed=42):
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)  # シャッフル
    idx = int(len(df) * ratio)
    return df.iloc[:idx], df.iloc[idx:]

def lambda_handler(event, context):
    # ===== 環境変数（デフォルト内蔵） =====
    DATA_BUCKET   = os.environ.get("DATA_BUCKET", "oyaizu-train")
    INPUT_PREFIX  = os.environ.get("INPUT_PREFIX", "raw")
    OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "mlops")
    CONFIG_PREFIX = os.environ.get("CONFIG_PREFIX", "config")

    MODEL_NAME    = os.environ.get("MODEL_NAME", "abalone-xgb")
    TRAINJOB_FILE = os.environ.get("TRAINJOB_FILE", "trainingjob.json")
    DEPLOY_LAMBDA_NAME = os.environ.get("DEPLOY_LAMBDA_NAME", "endpoint")

    # 実行IDと出力先
    exec_id = _now_id()
    exec_prefix = f"{OUTPUT_PREFIX}/{exec_id}"

    # 1) 入力CSV取得
    local_csv = "/tmp/abalone.csv"
    s3.download_file(DATA_BUCKET, f"{INPUT_PREFIX}/abalone.csv", local_csv)

    # 2) 前処理
    cols = ["Sex","Length","Diameter","Height","Whole","Shucked","Viscera","Shell","Rings"]
    df = pd.read_csv(local_csv, header=None, names=cols)
    df["SexCode"] = df["Sex"].replace({"I":0, "F":1, "M":2}).astype(int)
    features = ["Length","Diameter","Height","Whole","Shucked","Viscera","Shell","SexCode"]
    proc = pd.concat([df["Rings"], df[features]], axis=1)

    # 3) 80/20 分割（train_test_split 不使用）
    train_df, val_df = _split_train_val(proc, ratio=0.8, seed=42)

    # 4) CSV保存 & アップロード
    os.makedirs("/tmp/data", exist_ok=True)
    train_path = "/tmp/data/train.csv"
    val_path   = "/tmp/data/validation.csv"
    train_df.to_csv(train_path, header=False, index=False)
    val_df.to_csv(val_path,   header=False, index=False)

    train_key = f"{exec_prefix}/input/train/train.csv"
    val_key   = f"{exec_prefix}/input/validation/validation.csv"
    s3.upload_file(train_path, DATA_BUCKET, train_key)
    s3.upload_file(val_path,   DATA_BUCKET, val_key)

    # 5) trainingjob.json を取得・調整
    training_config = json.loads(
        s3.get_object(Bucket=DATA_BUCKET, Key=f"{CONFIG_PREFIX}/{TRAINJOB_FILE}")["Body"].read().decode("utf-8")
    )

    training_job_name = f"mlops-{MODEL_NAME}-{exec_id}"
    training_config["TrainingJobName"] = training_job_name

    # モデル出力先（この配下に <job>/output/model.tar.gz が生成される）
    training_config["OutputDataConfig"]["S3OutputPath"] = f"s3://{DATA_BUCKET}/{exec_prefix}/model"

    # 入力データURI
    training_config["InputDataConfig"][0]["DataSource"]["S3DataSource"]["S3Uri"] = f"s3://{DATA_BUCKET}/{train_key}"
    if len(training_config["InputDataConfig"]) > 1:
        training_config["InputDataConfig"][1]["DataSource"]["S3DataSource"]["S3Uri"] = f"s3://{DATA_BUCKET}/{val_key}"

    # 6) 学習開始
    sagemaker.create_training_job(**training_config)

    # 6.5) 学習完了まで待つ（Completed or Stopped を待機）
    waiter = sagemaker.get_waiter('training_job_completed_or_stopped')
    # 例: 60秒間隔 × 最大720回 = 12時間
    waiter.wait(
        TrainingJobName=training_job_name,
        WaiterConfig={'Delay': 60, 'MaxAttempts': 720}
    )

    # 状態確認（Completed 以外はエラー）
    desc = sagemaker.describe_training_job(TrainingJobName=training_job_name)
    status = desc["TrainingJobStatus"]
    assert status == "Completed", f"Training job not completed: {status}"

    # 学習成果物（model.tar.gz）の“確定”S3パス
    model_artifacts = desc["ModelArtifacts"]["S3ModelArtifacts"]

    # 7) ②を同期呼び出し（RequestResponse）
    deploy_event = {
        "status": "OK",
        "exec_id": exec_id,
        "train_s3": f"s3://{DATA_BUCKET}/{train_key}",
        "validation_s3": f"s3://{DATA_BUCKET}/{val_key}",
        "model_output_s3": f"s3://{DATA_BUCKET}/{exec_prefix}/model",
        "training_job_name": training_job_name,
        "model_data_url": model_artifacts  # ②はこれをそのまま ModelDataUrl に使う
    }

    resp = lambda_client.invoke(
        FunctionName=DEPLOY_LAMBDA_NAME,
        InvocationType="RequestResponse",  # 同期
        Payload=json.dumps(deploy_event).encode("utf-8")
    )
    deploy_result = json.load(resp["Payload"])

    # 8) まとめて返却
    return {
        "status": "OK",
        "exec_id": exec_id,
        "train_s3": f"s3://{DATA_BUCKET}/{train_key}",
        "validation_s3": f"s3://{DATA_BUCKET}/{val_key}",
        "model_output_s3": f"s3://{DATA_BUCKET}/{exec_prefix}/model",
        "training_job_name": training_job_name,
        "model_data_url": model_artifacts,
        "deploy_result": deploy_result
    }