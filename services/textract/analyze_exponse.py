import json
import boto3
textract = boto3.client('textract', region_name='us-east-1')

# 画像ファイルの内容やPDFから請求書を分析する
def analyze_expense(bucket, key):
    response = textract.analyze_expense(
        Document={
            'S3Object': 
                {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
    return response

def lambda_handler(event, context):
    bucket = 'my-bucket'
    key = 'my-key'
    textract_response = analyze_expense(bucket, key)

    # 住所
    address = [item['ValueDetection']['Text'] for item in textract_response['ExpenseDocuments'][0]['SummaryFields'] if 'ADDRESS' in item['Type']['Text']]
    # 請求額
    total = [item['ValueDetection']['Text'] for item in textract_response['ExpenseDocuments'][0]['SummaryFields'] if 'TOTAL' in item['Type']['Text']]
    # 請求者氏名
    biller_name = [item['ValueDetection']['Text'] for item in textract_response['ExpenseDocuments'][0]['SummaryFields'] if 'NAME' in item['Type']['Text']]
    # 請求書日付
    invoice_date = [item['ValueDetection']['Text'] for item in textract_response['ExpenseDocuments'][0]['SummaryFields'] if 'INVOICE_RECEIPT_DATE' in item['Type']['Text']]
    # 支払い期限
    payment_due_date = [item['ValueDetection']['Text'] for item in textract_response['ExpenseDocuments'][0]['SummaryFields'] if 'DUE_DATE' in item['Type']['Text']]
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
	    
	    
