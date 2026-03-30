## task1
**SageMaker-AI→Studio→JupyterLab→ab_ml_testing.ipynb**

### Step 3のセルを編集する(変更前はファイル名が間違っている)
```
model_url = S3Uploader.upload(
    local_path="xgb-churn-prediction-model.tar.gz", desired_s3_uri=f"s3://{bucket}/{prefix}"
)
model_url2 = S3Uploader.upload(
    local_path="xgb-churn-prediction-model2.tar.gz", desired_s3_uri=f"s3://{bucket}/{prefix}"
)
model_url, model_url2
```

## task2
### Step19のセルにコードを追加する
**※Step21は実行しなくてもよい**
```
sm.update_endpoint_weights_and_capacities(
    EndpointName=endpoint_name,
    DesiredWeightsAndCapacities=[
        {"DesiredWeight": 20, "VariantName": variant1["VariantName"]},
        {"DesiredWeight": 80, "VariantName": variant2["VariantName"]},
    ],
)
```

## task3(task2が完了した後に実行する)
### Step22のセルにコードを追加する
```
sm.update_endpoint_weights_and_capacities(
    EndpointName=endpoint_name,
    DesiredWeightsAndCapacities=[
        {"DesiredWeight": 0, "VariantName": variant1["VariantName"]},
        {"DesiredWeight": 1, "VariantName": variant2["VariantName"]},
    ],
)
```

