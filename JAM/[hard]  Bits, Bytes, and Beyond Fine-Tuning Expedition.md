## task1
### s3からファイルを取得する
```
cd SageMaker
aws s3 cp s3://labcode-<account-id>/lab-codes.zip .
unzip lab-codes.zip
```

### 回答(Step0の出力)
```
Amazon SageMaker
```

## task2
**lab-notebook.ipynbファイルを編集する**
### Task2-1
```
## [TASK2-1] Insert code to load a pre-trained model from Hugging Face's model hub. ##
model = AutoModelForCausalLM.from_pretrained(
    "databricks/dolly-v2-3b",
    # use_cache=False,
    device_map="auto", #"balanced",
    load_in_8bit=True,
)
```
### Task2-2
```
## [TASK2-2] Insert code to fine-tuning for Trainer object. please check huggingface official doc. ##
trainer.train()
```
### Task2-3
```
## [TASK2-3] Insert code here to define Model object. ##
model = Model(image_uri=image_uri,
              model_data=model_data,
              predictor_cls=sagemaker.djl_inference.DJLPredictor,
              role=aws_role)
```
### Task2-4
```
## [TASK2-4] Insert code here to deploy model,deploy option should be initial_instance_count=1, instance_type="ml.g4dn.2xlarge" ##
predictor = model.deploy(1, "ml.g4dn.2xlarge")
```

**APIGatewayに紐づくLambda関数(endpoint_test_function)の環境変数を編集する**

**出力プロパティの値を使用してWebアプリをテストする**

