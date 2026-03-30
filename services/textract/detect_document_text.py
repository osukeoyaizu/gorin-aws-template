import json
import boto3
textract = boto3.client('textract', region_name='ap-northeast-1')

# テキストを抽出する
def detect_document_text(bucket, key):
    response = textract.detect_document_text(
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
    bucket = 'my-s3-bucket'
    key = 'test.png'
    detect_document_text_response = detect_document_text(bucket, key)
    # フォーム抽出:(キーバリューペアを検出し、抽出する)
    for text in detect_document_text_response["Blocks"]:
        if text["BlockType"] == "LINE":
            print(text["Text"])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
	    
	    
