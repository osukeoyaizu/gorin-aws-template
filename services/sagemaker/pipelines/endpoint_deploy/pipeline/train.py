
"""
train.py

Trains an XGBoost regression model for the Abalone dataset and returns the S3 URI
of a SageMaker-serving-compatible model artifact (model.tar.gz) that contains
`xgboost-model` at the archive root.

Key points:
- No in-place mutation on input DataFrames
- Uses DMatrix for efficient training
- Supports CPU/GPU via tree_method
- Early stopping with validation set
- Saves model as `xgboost-model`, tars to `model.tar.gz`, uploads to S3
- Returns the S3 URI (s3://.../model.tar.gz)
"""

import io
import os
import tarfile
import tempfile
from typing import Tuple, Optional

import boto3
import numpy as np
import pandas as pd
import xgboost


def _to_dmatrix(df: pd.DataFrame) -> Tuple[xgboost.DMatrix, np.ndarray, np.ndarray]:
    """Split label (first column) and features to build a DMatrix safely."""
    # Work on a copy to avoid side effects
    y = df.iloc[:, 0].to_numpy()
    X = df.iloc[:, 1:].to_numpy()
    dmat = xgboost.DMatrix(X, label=y, feature_names=None)  # feature names optional
    return dmat, X, y


def _save_model_to_tar(booster: xgboost.Booster, s3_uri_prefix: str) -> str:
    """
    Save booster as `xgboost-model`, create model.tar.gz, upload to S3 and return its S3 URI.

    Args:
        booster: trained xgboost Booster
        s3_uri_prefix: e.g., 's3://my-bucket/abalone/models/2026-01-15-123456'

    Returns:
        s3_uri of uploaded tarball (ends with model.tar.gz)
    """
    # Parse bucket and key prefix
    if not s3_uri_prefix.startswith("s3://"):
        raise ValueError("s3_uri_prefix must start with 's3://'")
    _, _, bucket_and_key = s3_uri_prefix.partition("s3://")
    bucket, _, key_prefix = bucket_and_key.partition("/")
    key_prefix = key_prefix.rstrip("/")

    s3 = boto3.client("s3")

    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "xgboost-model")
        tar_path = os.path.join(tmpdir, "model.tar.gz")

        # Save booster
        booster.save_model(model_path)

        # Create tar.gz with `xgboost-model` at archive root (no subfolders)
        with tarfile.open(tar_path, mode="w:gz") as tar:
            tar.add(model_path, arcname="xgboost-model")

        # Upload to S3
        s3_key = f"{key_prefix}/model.tar.gz" if key_prefix else "model.tar.gz"
        s3.upload_file(tar_path, bucket, s3_key)

    return f"s3://{bucket}/{s3_key}"


def train(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    *,
    s3_output_prefix: str,          # 例: s3://<bucket>/abalone/models/<run-id> （必須）
    num_round: int = 200,
    objective: str = "reg:squarederror",  # ← reg:linear は廃止。回帰はこれ
    max_depth: int = 5,
    eta: float = 0.2,
    gamma: float = 4.0,
    min_child_weight: float = 6.0,
    subsample: float = 0.7,
    colsample_bytree: float = 1.0,
    reg_alpha: float = 0.0,
    reg_lambda: float = 1.0,
    seed: int = 42,
    use_gpu: bool = False,
    early_stopping_rounds: int = 20,
    eval_metric: str = "rmse",
) -> str:
    """
    Trains an XGBoost model and returns the S3 URI to model.tar.gz compatible with XGBoost DLC.

    Returns:
        str: S3 URI to model.tar.gz
    """
    # Build DMatrix (no in-place mutation)
    train_dmat, _, _ = _to_dmatrix(train_df)
    valid_dmat, _, _ = _to_dmatrix(validation_df)

    # XGBoost parameters
    params = {
        "objective": objective,
        "max_depth": max_depth,
        "eta": eta,
        "gamma": gamma,
        "min_child_weight": min_child_weight,
        "subsample": subsample,
        "colsample_bytree": colsample_bytree,
        "reg_alpha": reg_alpha,
        "reg_lambda": reg_lambda,
        "eval_metric": eval_metric,
        "tree_method": "gpu_hist" if use_gpu else "hist",
        "seed": seed,
    }

    evals_result = {}
    booster = xgboost.train(
        params=params,
        dtrain=train_dmat,
        num_boost_round=num_round,
        evals=[(train_dmat, "train"), (valid_dmat, "validation")],
        early_stopping_rounds=early_stopping_rounds,
        evals_result=evals_result,
        verbose_eval=False,
    )

    # Save & Upload (SageMaker XGBoost DLC expects 'xgboost-model' inside model.tar.gz)
    model_data_s3_uri = _save_model_to_tar(booster, s3_output_prefix)

    # （任意）ログ出力：最良イテレーション/メトリクス
    best_iter = booster.best_iteration
    best_score = booster.best_score
    print(f"[train] best_iteration={best_iter}, best_score={best_score}, eval_metric={eval_metric}")
    print(f"[train] model_data_s3_uri={model_data_s3_uri}")

    return model_data_s3_uri
