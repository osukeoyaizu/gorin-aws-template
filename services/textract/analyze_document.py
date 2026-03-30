
import json
import boto3

textract = boto3.client('textract', region_name='us-west-2')

# PDFや画像からフォーム情報を分析する
def analyze_document(bucket, key):
    response = textract.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        FeatureTypes=['FORMS', 'TABLES']  # フォームとテーブルを解析
    )
    return response

def lambda_handler(event, context):
    bucket = 'loan-processing-applications-044257918205'
    key = 'sample_loan_application.pdf'
    textract_response = analyze_document(bucket, key)

    # キーと値のペアを抽出
    extracted_data = {}
    for block in textract_response.get('Blocks', []):
        if block['BlockType'] == 'KEY_VALUE_SET' and 'EntityTypes' in block and 'KEY' in block['EntityTypes']:
            key_text = ''
            value_text = ''
            # キーのテキスト取得
            for rel in block.get('Relationships', []):
                if rel['Type'] == 'CHILD':
                    for id in rel['Ids']:
                        child_block = next((b for b in textract_response['Blocks'] if b['Id'] == id), None)
                        if child_block and 'Text' in child_block:
                            key_text += child_block['Text'] + ' '
            # 値のテキスト取得
            for rel in block.get('Relationships', []):
                if rel['Type'] == 'VALUE':
                    for id in rel['Ids']:
                        value_block = next((b for b in textract_response['Blocks'] if b['Id'] == id), None)
                        if value_block:
                            for vrel in value_block.get('Relationships', []):
                                if vrel['Type'] == 'CHILD':
                                    for vid in vrel['Ids']:
                                        child_block = next((b for b in textract_response['Blocks'] if b['Id'] == vid), None)
                                        if child_block and 'Text' in child_block:
                                            value_text += child_block['Text'] + ' '
            if key_text.strip():
                extracted_data[key_text.strip()] = value_text.strip()

    print(extracted_data)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Document analyzed successfully',
            'extractedData': extracted_data
        })
    }
