import boto3
import sagemaker
import numpy as np
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer
from colorama import init, Fore, Style, Back
import time
import csv
import io

init(autoreset=True)  

def blink_text(text, color, times=3):
    """Create blinking effect"""
    for _ in range(times):
        print(f"\r{Style.BRIGHT}{color}{text}", end="", flush=True)
        time.sleep(0.5)
        print("\r" + " " * len(text), end="", flush=True)
        time.sleep(0.5)
    print(f"\r{Style.BRIGHT}{color}{text}")

def predict_single_record(endpoint_name, record):
    try:
        predictor = sagemaker.predictor.Predictor(
            endpoint_name=endpoint_name,
            sagemaker_session=sagemaker.Session(),
            serializer=CSVSerializer(),
            deserializer=CSVDeserializer()
        )
        
        if isinstance(record, list):
            record = np.array(record)
        record = record.reshape(1, -1)
        
        csv_record = ','.join(map(str, record[0]))
        predictions = predictor.predict(csv_record)
        probability = float(predictions[0][0])
        
        if probability > 0.5:
            outcome = "Win"
        else:
            outcome = "Lose"
        
        return outcome, probability
    
    except Exception as e:
        print(f"{Fore.RED}Error during prediction: {str(e)}")
        return None, None

def save_results_to_s3(bucket_name, outcome, confidence):
    try:
        s3 = boto3.client('s3')
        
        
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['Prediction Result', 'Confidence'])
        csv_writer.writerow([outcome, f"{confidence:.1f}%"])
        
        
        s3.put_object(
            Bucket=bucket_name,
            Key='results/prediction.csv',
            Body=csv_buffer.getvalue()
        )
        print(f"{Fore.GREEN}Results saved to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"{Fore.RED}Error saving results to S3: {str(e)}")

if __name__ == "__main__":
    endpoint_name = "#TODO"
    bucket_name = "#TODO"  
    
    sample_record = [2, 2, 0.99, 0.67, 50, 20, 20, 20]
    
    print(f"\n{Fore.CYAN}🏀 Analyzing Game Statistics...")
    print(f"{Fore.YELLOW}Home Team vs Away Team")
    print(f"{Fore.WHITE}FG%: {sample_record[2]*100:.1f}% vs {sample_record[3]*100:.1f}%")
    print(f"REB: {sample_record[4]} vs {sample_record[5]}")
    print(f"AST: {sample_record[6]} vs {sample_record[7]}\n")
    
    outcome, probability = predict_single_record(endpoint_name, sample_record)
    
    if outcome and probability is not None:
        print(f"{Fore.CYAN}Prediction Result:")
        if outcome == "Win":
            blink_text("🏆 HOME TEAM WINS! 🏆", Fore.GREEN)
        else:
            blink_text("❌ HOME TEAM LOSES! ❌", Fore.RED)
        
        confidence = probability * 100
        print(f"{Fore.YELLOW}Confidence: {Fore.WHITE}{confidence:.1f}%")
        
        
        results = {
            'outcome': outcome,
            'probability': probability,
            'stats': {
                'fg_percent_home': sample_record[2]*100,
                'fg_percent_away': sample_record[3]*100,
                'rebounds_home': sample_record[4],
                'rebounds_away': sample_record[5],
                'assists_home': sample_record[6],
                'assists_away': sample_record[7]
            }
        }
        
        
        save_results_to_s3(bucket_name, outcome, confidence)
    else:
        print(f"{Fore.RED}Prediction failed")
        results = None