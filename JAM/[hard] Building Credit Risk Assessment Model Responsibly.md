## task1
**2つ目のセルのBUCKETを課題用バケット名にする**

### 回答方法
**auc_score|endpoint_name**

## task2
### Data Config code block
```
bias_report_output_path = f's3://{BUCKET}/clarify-reports'
bias_data_config = clarify.DataConfig(
    s3_data_input_path=train_s3_path,
    s3_output_path=bias_report_output_path,
    label=LABEL_COLUMN,
    headers=DATASET_COLUMNS,
    dataset_type='text/csv',
)
```
### Bias Config code block
```
bias_config = clarify.BiasConfig(
    label_values_or_threshold=[1],    # Label 1 as positive class (good credit risk)
    facet_name='personal_status_sex',
)
```
### Model Config code block
```
model_config = clarify.ModelConfig(
    model_name=pipeline_model.name,  # specify the inference pipeline model name
    instance_type=INSTANCE_TYPE,
    instance_count=1,
    accept_type='text/csv',
)
```
### Model Predicted Label Config code block
```
predictions_config = clarify.ModelPredictedLabelConfig(label=None, probability=0)  # XGBoost returns probability value (not label) as prediction
```
### Run Clarify bias job code block
```
bias_job_name = f'clarify-bias-{dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
clarify_processor.run_bias(
    job_name=bias_job_name,
    data_config=bias_data_config,
    bias_config=bias_config,
    model_config=model_config,
    model_predicted_label_config=predictions_config,
    pre_training_methods='all',
    post_training_methods='all',
)
bias_job_name
```

### 回答方法
**base_bias_reportフォルダのreport.html内のpersonal_status_sex == 1のDifference in Positive Proportions in Predicted Labels(DPPL)の値をコピーする**

**dppl_score|clarify_job_name**

## task3
### SHAP Config code block
```
shap_config = clarify.SHAPConfig(
    baseline=[baseline],
    num_samples=2500,
    agg_method='mean_abs',
    use_logit=True,
)
```
### Data Config code block
```
explainability_output_path = f's3://{BUCKET}/clarify-explainability'

explainability_data_config = clarify.DataConfig(
    s3_data_input_path=test_s3_path,
    s3_output_path=explainability_output_path,
    label=LABEL_COLUMN,
    headers=DATASET_COLUMNS,
    dataset_type='text/csv',
)
```
### Run Clarify Explainability code block
```
explainability_job_name = f'clarify-explainability-{dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
clarify_processor.run_explainability(
    job_name=explainability_job_name,
    data_config=explainability_data_config,
    model_config=model_config,
    explainability_config=shap_config,
)
explainability_job_name
```

### 回答方法
**base_explainability_reportフォルダのreport.html内の横棒グラフの特徴量属性を確認する**

**top_8_features|clarify_job_name**

**例:status,duration,savings,amount,credit_history,age,employment_duration,installment_rate|clarify_job_name**


## task4()
**challenge_notebook.ipynb**
### Preprocessing job code block
```
sklearn_processor = SKLearnProcessor(
    sagemaker_session=sagemaker_session,
    role=role,
    framework_version='1.2-1',
    instance_type=INSTANCE_TYPE,
    instance_count=1,
)

PROC_INPUT_PATH = '/opt/ml/processing/input'
base_proc_job_name = f'responsible-ai-jam-processing-{dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
sklearn_processor.run(
    inputs=[
        ProcessingInput(source=f's3://{BUCKET}/{S3_DATA_PREFIX}/', destination=PROC_INPUT_PATH),
    ],
    outputs=[
        ProcessingOutput(output_name='processing_model', source='/opt/ml/processing/model'),
        ProcessingOutput(output_name='train', source='/opt/ml/processing/train'),
        ProcessingOutput(output_name='validation', source='/opt/ml/processing/validation'),
    ],
    code='scripts/preprocessor2.py',
    job_name=base_proc_job_name,

)
```

### Training XGBoost code block
```
xgb_train.fit(
    job_name=training_job_name,
    inputs={
        'train': TrainingInput(
            s3_data=preprocessed_train_data,
            content_type='text/csv',
        ),
        'validation': TrainingInput(
            s3_data=preprocessed_val_data,
            content_type='text/csv',
        ),
    },
)
```

### Create pipeline model code block
```
sklearn_model = SKLearnModel(
   sagemaker_session=sagemaker_session,
   role=role,
   framework_version='1.2-1',
   model_data=processing_model_file,
   entry_point='preprocessor_inference.py', 
   source_dir='scripts/', 
)

xgboost_model = xgb_train.create_model(
    role=role,
    image_uri=image_uri,
    predictor_cls=XGBoostPredictor,
)

pipeline_model_name = f'responsible-model-{dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
pipeline_model = PipelineModel(
    sagemaker_session=sagemaker_session,
    role=role,
    models=[sklearn_model, xgboost_model],
    name=pipeline_model_name,
)
pipeline_model_name
```

### 回答方法
**auc_score|endpoint_name**


## task5
### Model Config code block
```
model_config = clarify.ModelConfig(
    model_name=pipeline_model.name,  # specify the inference pipeline model name
    instance_type=INSTANCE_TYPE,
    instance_count=1,
    accept_type='text/csv',
)
```

### SHAP Config code block
```
shap_config = clarify.SHAPConfig(
    baseline=[baseline],
    num_samples=2500,
    agg_method='mean_abs',
    use_logit=True,
)
```

### Data Config code block
```
explainability_output_path = f's3://{BUCKET}/responsible-clarify-explainability'
explainability_data_config = clarify.DataConfig(
    s3_data_input_path=test_s3_path,
    s3_output_path=explainability_output_path,
    label=LABEL_COLUMN,
    headers=DATASET_COLUMNS,
    dataset_type='text/csv',
)
```
### Run Clarify Explainability code block
```
explainability_job_name = f'clarify-explainability-{dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
clarify_processor.run_explainability(
    job_name=explainability_job_name,
    data_config=explainability_data_config,
    model_config=model_config,
    explainability_config=shap_config,
)
explainability_job_name
```

### 回答方法
**responsible_explainability_reportフォルダのreport.html内の横棒グラフの特徴量属性を確認する**

**top_8_features|clarify_job_name**

**例:status,duration,savings,amount,credit_history,employment_duration,purpose,installment_rate|clarify_job_name**
