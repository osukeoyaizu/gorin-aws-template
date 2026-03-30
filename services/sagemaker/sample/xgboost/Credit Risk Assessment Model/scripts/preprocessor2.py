import joblib
import os
import tarfile

import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

LABEL_COLUMN = 'credit_risk'
PROC_PATH = '/opt/ml/processing/'
PROC_INPUT_PATH = f'{PROC_PATH}input/'
PROC_MODEL_PATH = f'{PROC_PATH}model/'
PROC_MODEL_FILENAME = 'model.joblib'


if __name__ == "__main__":
    train_df = pd.read_csv(f'{PROC_INPUT_PATH}train.csv')
    val_df = pd.read_csv(f'{PROC_INPUT_PATH}validation.csv')

    # Perform one-hot encoding to the following columns
    # We also drop personal_status_sex and age columns
    column_preprocessor = make_column_transformer(
        (OneHotEncoder(),['credit_history',
                          'purpose',
                          'other_debtors',
                          'property',
                          'other_installment_plans',
                          'housing',
                          'job',
                          'telephone',
                          'foreign_worker',
                         ]),
        ('drop', ['personal_status_sex','age']), # dropping 'personal_status_sex', and 'age' columns
        remainder='passthrough',
    )

    y_train = train_df[LABEL_COLUMN]
    X_train = train_df.drop(LABEL_COLUMN, axis=1, inplace=False)
    
    y_val = val_df[LABEL_COLUMN]
    X_val = val_df.drop(LABEL_COLUMN, axis=1, inplace=False)
    
    featurizer_model = column_preprocessor.fit(X_train)
    Xf_train = featurizer_model.transform(X_train)
    Xf_val = featurizer_model.transform(X_val)

    # SageMaker XGBoost built-in algorithm expect the class label to be in the first column
    preprocessed_train_df = pd.concat([y_train, pd.DataFrame(Xf_train)], axis=1).reset_index(drop=True)
    preprocessed_val_df = pd.concat([y_val, pd.DataFrame(Xf_val)], axis=1).reset_index(drop=True)
    
    # SageMaker XGBoost built-in algorithm does not require header in the csv file.
    preprocessed_train_df.to_csv(f'{PROC_PATH}train/train.csv', header=False, index=False)
    preprocessed_val_df.to_csv(f'{PROC_PATH}validation/validation.csv', header=False, index=False)

    joblib.dump(featurizer_model, PROC_MODEL_FILENAME)
    with tarfile.open(f'{PROC_MODEL_PATH}model.tar.gz', 'w:gz') as tar_handle:
        tar_handle.add(PROC_MODEL_FILENAME)