## 前提条件
JupyterLabのImage:Sagemaker Distribution 3.4.2

### ターミナルで以下のコマンド実行
※依存関係問題解消のため
```
pip uninstall -y \
  sagemaker sagemaker-core sagemaker-train sagemaker-serve sagemaker-mlops sagemaker_schema_inference_artifacts \
  autogluon-multimodal autogluon-timeseries \
  sparkmagic sagemaker-studio-analytics-extension \
  transformers
```
```
pip install \
  "sagemaker==2.245.0" \
  "boto3==1.37.1" "botocore==1.37.1" \
  "s3fs==2024.12.0" "aiobotocore==2.21.1" \
  "pandas>=2.3.1" "numpy>=1.26.4" "scikit-learn>=1.7.1" \
  "xgboost==2.1.4" \
  "graphene"
```

#### 確認用
```
python - <<'PY'
import sagemaker, sys
print("sagemaker version:", sagemaker.__version__)
print("sagemaker file   :", getattr(sagemaker, "__file__", "NA"))
import boto3, botocore, s3fs, aiobotocore
print("boto3/botocore   :", boto3.__version__, botocore.__version__)
print("s3fs/aiobotocore :", s3fs.__version__, aiobotocore.__version__)
PY
```

## コードの修正ポイント(endpoint_deploy)
pipeline.py

96行目:SQSのARN

101行目:ステータスチェック用LambdaのARN

110行目:エンドポイントの作成用LambdaのARN
