import json
import tarfile
import os
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error

# Paths
model_dir = "/opt/ml/processing/model"
val_dir = "/opt/ml/processing/validation"
eval_dir = "/opt/ml/processing/evaluation"

os.makedirs(eval_dir, exist_ok=True)

# Extract model
with tarfile.open(f"{model_dir}/model.tar.gz") as tar:
    tar.extractall(path=model_dir)

# Load model
model = xgb.Booster()
model.load_model(f"{model_dir}/xgboost-model")

# Load validation data
df = pd.read_csv(f"{val_dir}/validation.csv", header=None)
X = df.iloc[:, 1:]
y = df.iloc[:, 0]

# Predict
dval = xgb.DMatrix(X)
preds = model.predict(dval)

rmse = np.sqrt(mean_squared_error(y, preds))

# Save metrics
metrics = {
    "regression_metrics": {
        "rmse": {
            "value": rmse,
            "standard_deviation": 0.0
        }
    }
}

with open(f"{eval_dir}/metrics.json", "w") as f:
    json.dump(metrics, f)