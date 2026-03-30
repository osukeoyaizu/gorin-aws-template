
"""
evaluate.py

Evaluates an XGBoost model stored in S3 (model.tar.gz) on a test dataset.
- Loads model from S3 (expects 'xgboost-model' inside tar)
- Computes predictions on test dataset
- Calculates regression metrics (MSE, RMSE, Std of residuals)
- Returns structured evaluation report as dict
"""

import os
import tarfile
import tempfile
import boto3
import numpy as np
import pandas as pd
import xgboost
from sklearn.metrics import mean_squared_error


def _load_booster_from_s3(model_s3_uri: str) -> xgboost.Booster:
    """Download model.tar.gz from S3, extract xgboost-model, and load Booster."""
    if not model_s3_uri.startswith("s3://"):
        raise ValueError("model_s3_uri must start with 's3://'")
    _, _, bucket_and_key = model_s3_uri.partition("s3://")
    bucket, _, key = bucket_and_key.partition("/")

    s3 = boto3.client("s3")

    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = os.path.join(tmpdir, "model.tar.gz")
        model_path = os.path.join(tmpdir, "xgboost-model")

        # Download tar.gz
        s3.download_file(bucket, key, tar_path)

        # Extract xgboost-model
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extract("xgboost-model", path=tmpdir)

        # Load Booster
        booster = xgboost.Booster()
        booster.load_model(model_path)
        return booster


def evaluate(model_data_s3_uri: str, test_df: pd.DataFrame) -> dict:
    """
    Args:
        model_data_s3_uri: S3 URI to model.tar.gz (e.g., s3://bucket/path/model.tar.gz)
        test_df: pandas DataFrame with label in first column

    Returns:
        dict: evaluation report
    """
    # Load model from S3
    booster = _load_booster_from_s3(model_data_s3_uri)

    # Prepare test data (no inplace mutation)
    y_test = test_df.iloc[:, 0].to_numpy()
    X_test = test_df.iloc[:, 1:].to_numpy()

    # Predict
    dtest = xgboost.DMatrix(X_test)
    predictions = booster.predict(dtest)

    # Metrics
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    std_residuals = np.std(y_test - predictions)

    report_dict = {
        "regression_metrics": {
            "mse": {"value": mse},
            "rmse": {"value": rmse},
            "residual_std": {"value": std_residuals},
        }
    }

    print(f"[evaluate] report: {report_dict}")
    return report_dict
