
# register.py
# - Serveモードを使用せず、XGBoost 1.7 系 DLC の既定ハンドラで安全に登録。
# - requirements.txt は一切配布しない（= 推論コンテナで pip は走らない）。

import json
import s3fs
import sagemaker
from sagemaker import ModelMetrics, MetricsSource
from sagemaker.s3_utils import s3_path_join
from sagemaker.utils import unique_name_from_base
from sagemaker.model import Model  # XGBoostModel を使わず汎用 Model + image_uri で組む


def register(
    model_data_s3_uri: str,
    evaluation: dict,
    model_approval_status: str,
    model_package_group_name: str,
    bucket: str,
    role_arn: str = None,
) -> str:
    """
    Args:
        model_data_s3_uri: 学習成果物(S3)のURI (例: s3://<bucket>/training-output/model.tar.gz)
        evaluation: モデル評価 dict（JSON 化して S3 へ保存）
        model_approval_status: "Approved" | "Rejected" | "PendingManualApproval"
        model_package_group_name: 既存/新規の Model Package Group 名
        bucket: 評価レポートをアップロードする S3 バケット名
        role_arn: モデルが参照する実行ロール（省略時は sagemaker.Session のロールを使用）

    Returns:
        str: 登録された Model Package の ARN
    """
    sm_sess = sagemaker.Session()
    region = sm_sess.boto_region_name

    # 実行ロールの解決（Studio等/非Studioの両対応）
    try:
        resolved_role = role_arn or sagemaker.get_execution_role()
    except Exception:
        resolved_role = role_arn or sm_sess.get_caller_identity_arn()

    # 1) XGBoost 1.7 系の推論イメージ（CPU）
    image_uri = sagemaker.image_uris.retrieve(
        framework="xgboost",
        region=region,
        version="1.7-1",
    )

    # 2) 評価レポートを S3 にアップロード（Model Metrics 用）
    eval_file_name = unique_name_from_base("evaluation")
    eval_report_s3_uri = s3_path_join("s3://", bucket, f"evaluation-report/{eval_file_name}.json")

    s3_fs = s3fs.S3FileSystem()
    with s3_fs.open(eval_report_s3_uri, "wb") as f:
        f.write(json.dumps(evaluation).encode("utf-8"))

    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri=eval_report_s3_uri,
            content_type="application/json",
        )
    )

    # 3) モデル定義（汎用 Model + image_uri + model_data）
    #    - XGBoost DLC の標準サーバを使うので、entry_point / code 配布は不要
    base_model = Model(
        image_uri=image_uri,
        model_data=model_data_s3_uri,
        role=resolved_role,
        sagemaker_session=sm_sess,
        env={},     # 必要に応じて環境変数。不要なら空のまま
        name=None,  # 自動命名
    )

    # 4) Model Registry へ登録
    model_package = base_model.register(
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.xlarge"],
        transform_instances=["ml.m5.xlarge"],
        model_package_group_name=model_package_group_name,
        approval_status=model_approval_status,
        model_metrics=model_metrics,
        # VPC や DataCapture が必要なら追加引数を渡す
    )

    print(f"Registered Model Package ARN: {model_package.model_package_arn}")
    return model_package.model_package_arn 