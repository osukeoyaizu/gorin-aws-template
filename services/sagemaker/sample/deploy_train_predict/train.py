import pandas as pd
import boto3
import sagemaker
from sagemaker import get_execution_role
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prepare_data_for_xgboost():
    """Prepare CSV data for XGBoost training"""
    
    # Setup with specific bucket and key
    s3 = boto3.client('s3')
    bucket_name = '#TODO'
    file_key = '#TODO' #Find the file_key in your S3 bucket where you exported the cleaned data. The file_key follows this format: "clean/output_{{########}}/{{file_name}}.csv"
    
    try:
        # Read the data from S3
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        
        # Split data into train and validation (80-20 split)
        train_size = int(0.8 * len(df))
        train_df = df[:train_size]
        val_df = df[train_size:]
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col not in ['GAME_ID', 'outcome']]
        
        # Prepare training data
        train_features = train_df[feature_columns]
        train_labels = train_df['outcome']
        prepared_train = pd.concat([train_labels, train_features], axis=1)
        
        # Prepare validation data
        val_features = val_df[feature_columns]
        val_labels = val_df['outcome']
        prepared_val = pd.concat([val_labels, val_features], axis=1)
        
        # Save prepared data locally
        prepared_train.to_csv('prepared_train.csv', index=False, header=False)
        prepared_val.to_csv('prepared_validation.csv', index=False, header=False)
        
        # Upload prepared data back to S3
        s3.upload_file('prepared_train.csv', bucket_name, 'prepared/train.csv')
        s3.upload_file('prepared_validation.csv', bucket_name, 'prepared/validation.csv')
        
        return True
        
    except Exception as e:
        logger.error(f"Error in data preparation: {str(e)}")
        return False

def cleanup_training_resources(training_job_name):
    """Clean up training job and associated resources"""
    try:
        sagemaker_client = boto3.client('sagemaker')
        sagemaker_client.stop_training_job(TrainingJobName=training_job_name)
        logger.info(f"Successfully stopped training job: {training_job_name}")
    except Exception as e:
        logger.error(f"Error cleaning up training job: {str(e)}")

def main():
    try:
        # Get the role and create a session
        role = get_execution_role()
        session = sagemaker.Session()
        
        # Get the XGBoost container
        container = sagemaker.image_uris.retrieve(
            framework='#TODO',
            region=session.boto_region_name,
            version='1.5-1'
        )
        
        bucket_name = '#TODO' 
        
        # Configure the estimator
        xgb = sagemaker.estimator.Estimator(
            container,
            role,
            instance_count=1,
            instance_type='#TODO',
            output_path=f's3://{bucket_name}/output',
            hyperparameters={
                'objective': 'binary:logistic',
                'max_depth': 5,
                'eta': 0.2,
                'num_round': 100,
                'eval_metric': 'auc'
            }
        )

        # Prepare the data
        if not prepare_data_for_xgboost():
            logger.error("Data preparation failed. Aborting training.")
            return
            
        # Define training inputs
        train_input = sagemaker.inputs.TrainingInput(
            s3_data=f's3://{bucket_name}/prepared/train.csv',
            content_type='text/csv',
            s3_data_type='S3Prefix'
        )

        validation_input = sagemaker.inputs.TrainingInput(
            s3_data=f's3://{bucket_name}/prepared/validation.csv',
            content_type='text/csv',
            s3_data_type='S3Prefix'
        )

        try:
            # Train the model
            xgb.fit({
                'train': train_input,
                'validation': validation_input
            })
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            if hasattr(xgb, '_current_job_name'):
                cleanup_training_resources(xgb._current_job_name)
            raise

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")