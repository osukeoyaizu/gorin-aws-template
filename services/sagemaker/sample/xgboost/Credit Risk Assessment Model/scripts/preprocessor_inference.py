import pandas as pd
import os
import json
import joblib
from io import StringIO

try:
    from sagemaker_containers.beta.framework import (
        content_types,
        encoders,
        worker,
        server,
    )
except ImportError:
    pass


# we exclude the class label `credit_risk`
credit_columns = [
    "status",
    "duration",
    "credit_history",
    "purpose",
    "amount",
    "savings",
    "employment_duration",
    "installment_rate",
    "personal_status_sex",
    "other_debtors",
    "present_residence",
    "property",
    "age",
    "other_installment_plans",
    "housing",
    "number_credits",
    "job",
    "people_liable",
    "telephone",
    "foreign_worker",
]


def input_fn(input_data, content_type):
    """Parse input data payload.
    We currently only take csv input. 
    """
    if content_type == 'text/csv':
        # Read the raw input data as CSV.
        df = pd.read_csv(StringIO(input_data),
                         names=credit_columns,
                         header=None)
        print(df)
        return df
    else:
        raise ValueError(f'{content_type} not supported by the script!')


def output_fn(prediction, accept):
    """Format prediction output
    The default accept/content-type between containers for serial inference is JSON.
    But, our XGBoost uses text/csv. We want to set the ContentType or mimetype as text/csv so the XGBoost
    container can read the response payload correctly.
    """
    accept = "text/csv"
    if accept == "application/json":
        print("preprocessing output as application/json")
        instances = []
        for row in prediction.tolist():
            instances.append(row)
        json_output = {"instances": instances}

        return worker.Response(json.dumps(json_output), mimetype=accept)
    elif accept == "text/csv":
        print("preprocessing output as text/csv")
        return worker.Response(encoders.encode(prediction, accept), mimetype=accept)
    else:
        raise RuntimeException(f'{accept} accept type is not supported by this script.')


def predict_fn(input_data, model):
    """Preprocess input data
    We implement this because the default predict_fn uses .predict(), but our model is a preprocessor
    so we want to use .transform().
    """
    print('Predict')
    print(input_data)
    features = model.transform(input_data)
    return features


def model_fn(model_dir):
    """Deserialize fitted preprocessor model"""
    print("load model")
    print(os.listdir(model_dir))
    print(joblib.__version__)
    preprocessor = joblib.load(os.path.join(model_dir, 'model.joblib'))
    print('Preprocessor loaded successfully.')
    return preprocessor