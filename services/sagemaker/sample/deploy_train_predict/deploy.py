import boto3
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import sagemaker
import json
import io
import time
import csv
from sagemaker import get_execution_role
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer

def evaluate_model(endpoint_name):
    try:
        # Initialize S3 client
        s3 = boto3.client('s3')
        bucket_name = '#TODO'
        
        # Get the validation data
        obj = s3.get_object(Bucket=bucket_name, Key='prepared/validation.csv')
        validation_data = pd.read_csv(io.BytesIO(obj['Body'].read()), header=None)
        
        print("\nValidation Data Summary:")
        print(f"Validation data shape: {validation_data.shape}")
        print(f"Validation data columns: {validation_data.columns}")
        print(f"Validation data types: {validation_data.dtypes}")
        
        # Separate features and target from validation data
        X_val = validation_data.iloc[:, 1:]  # All columns except first
        y_val = validation_data.iloc[:, 0]   # First column is target
        
        # Get the model predictions
        predictor = sagemaker.predictor.Predictor(
            endpoint_name=endpoint_name,
            sagemaker_session=sagemaker.Session(),
            serializer=CSVSerializer(),
            deserializer=CSVDeserializer()
        )
        
        # Convert features to CSV format
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerows(X_val.values)
        csv_data = csv_buffer.getvalue()
        
        # Make predictions
        predictions = predictor.predict(csv_data)
        
        print("\nPredictions Overview:")
        print(f"Predictions shape: {np.array(predictions).shape}")
        print(f"Predictions type: {type(predictions)}")
        print(f"First few predictions: {predictions[:5]}")
        
        # Convert string predictions to float values
        float_predictions = [float(pred[0]) for pred in predictions]
        
        # Convert to numpy array and make binary predictions
        predictions_array = np.array(float_predictions)
        binary_predictions = (predictions_array > 0.5).astype(int)
        
        # Calculate metrics
        accuracy = accuracy_score(y_val, binary_predictions)
        conf_matrix = confusion_matrix(y_val, binary_predictions)
        class_report = classification_report(y_val, binary_predictions)
        
        # Print results
        print("\nModel Evaluation Results:")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nConfusion Matrix:")
        print(conf_matrix)
        print("\nClassification Report:")
        print(class_report)
        
        # Save evaluation results to S3
        evaluation_results = {
            'accuracy': float(accuracy),
            'confusion_matrix': conf_matrix.tolist(),
            'classification_report': class_report
        }
        
        # Save results to S3
        s3.put_object(
            Bucket=bucket_name,
            Key='model_evaluation/evaluation_results.json',
            Body=json.dumps(evaluation_results)
        )
        
        return evaluation_results
        
    except Exception as e:
        print(f"Error during model evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def create_endpoint_and_evaluate():
    try:
        # Get the latest training job name
        training_job_name = '#TODO'
        bucket_name= '#TODO'
        if not training_job_name:
            raise Exception("No training job found")
        
        print(f"\nLatest training job: {training_job_name}")
        
        # Get the XGBoost image URI
        region = boto3.Session().region_name
        container = sagemaker.image_uris.retrieve("xgboost", region, "1.5-1")
        
        # Create model
        model = sagemaker.model.Model(
            image_uri=container,
            model_data=f's3://{bucket_name}/output/{training_job_name}/output/model.tar.gz',
            role=get_execution_role(),
            sagemaker_session=sagemaker.Session()
        )
        
        # Deploy model to endpoint
        endpoint_name = f'xgboost-endpoint-{int(time.time())}'
        model.deploy(
            initial_instance_count=1,
            instance_type='#TODO',
            endpoint_name=endpoint_name,
            content_type='text/csv'
        )
        
        print(f"\nModel deployed to endpoint: {endpoint_name}")
        
        # Wait for endpoint to be ready
        waiter = boto3.client('sagemaker').get_waiter('endpoint_in_service')
        waiter.wait(EndpointName=endpoint_name)
        
        print("\nEndpoint is ready. Starting evaluation...")
        
        # Evaluate the model
        evaluation_results = evaluate_model(endpoint_name)
        
        return evaluation_results
        
    except Exception as e:
        print(f"Error in create_endpoint_and_evaluate: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def cleanup_endpoint(endpoint_name):
    try:
        sagemaker_client = boto3.client('sagemaker')
        sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
        print(f"\nEndpoint {endpoint_name} has been deleted.")
    except Exception as e:
        print(f"Error deleting endpoint: {str(e)}")

# Execute the evaluation
if __name__ == "__main__":
    try:
        # Create endpoint and evaluate
        print("\nStarting model evaluation...")
        results = create_endpoint_and_evaluate()
        
        if results:
            print("\nEvaluation completed successfully!")
            print(f"Model Accuracy: {results['accuracy']:.4f}")
        else:
            print("\nEvaluation failed!")
            
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        import traceback
        traceback.print_exc()