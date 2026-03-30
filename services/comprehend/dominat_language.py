import json
import boto3

comprehend = boto3.client('comprehend', region_name='ap-northeast-1')

# 言語検出
def detect_dominant_language(text):
    response = comprehend.detect_dominant_language(Text=text)
    return response


def lambda_handler(event, context):
    # 変更内容
    text = 'Amazon Comprehend is a natural language processing (NLP) service that uses machine learning to find insights and relationships in text.'

    # 言語検出
    detect_dominant_language_response = detect_dominant_language(text)
    language_code_list = []
    for language in detect_dominant_language_response['Languages']:
        language_code_dict = {}
        language_code_dict['LanguageCode'] = language['LanguageCode']
        language_code_dict['Score'] = language['Score']
        language_code_list.append(language_code_dict)

    language_code = detect_dominant_language_response['Languages'][0]['LanguageCode']
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
