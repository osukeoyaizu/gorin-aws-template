## task1
### S3(loan-processing-applications-{アカウントID})にイベント通知を作成する
Event Name:任意

Suffix:.pdf

Event types:All

Destination:Lambda(loan-processing-document-processor)


## task2
### Lambda(loan-processing-document-processor)を編集する
```
import json
import boto3
import uuid
import os
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
textract = boto3.client('textract')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        # Get S3 object details
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        # Generate application ID
        app_id = str(uuid.uuid4())
        
        # Call Textract to detect document text (basic extraction only)
        response = textract.analyze_document(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}},
            FeatureTypes=['FORMS', 'TABLES']
        )
        
        # Extract key information
        extracted_data = extract_loan_data(response)
        extracted_data['applicationId'] = app_id
        extracted_data['documentKey'] = key
        
        # Invoke eligibility processor
        lambda_client.invoke(
            FunctionName=os.environ['ELIGIBILITY_FUNCTION'],
            InvocationType='Event',
            Payload=json.dumps(extracted_data)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'applicationId': app_id,
                'message': 'Document processed, eligibility check initiated'
            })
        }
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def extract_loan_data(textract_response):
    # Simplified extraction logic
    extracted = {}
    
    # Extract text blocks
    for block in textract_response.get('Blocks', []):
        if block['BlockType'] == 'LINE':
            text = block.get('Text', '').lower()
            
            # Simple pattern matching
            if 'name' in text and ':' in text:
                extracted['name'] = text.split(':')[1].strip()
            elif 'income' in text and ':' in text:
                try:
                    extracted['income'] = float(''.join(filter(str.isdigit, text.split(':')[1])))
                except:
                    pass
            elif 'loan amount' in text and ':' in text:
                try:
                    extracted['loan_amount'] = float(''.join(filter(str.isdigit, text.split(':')[1])))
                except:
                    pass
            elif 'tenure' in text and ':' in text:
                try:
                    extracted['tenure'] = int(''.join(filter(str.isdigit, text.split(':')[1])))
                except:
                    pass
    
    return extracted

```

## task3
### Lambda(loan-processing-eligibility-processor)の環境変数を設定する
Key: DYNAMODB_TABLE

Value: loan-processing-applications
