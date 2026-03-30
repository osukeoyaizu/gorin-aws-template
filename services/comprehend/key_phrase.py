import json
import boto3

client = boto3.client('comprehend', region_name='ap-northeast-1')

def detect_key_phrases(text, language_code):
    response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    return response


def lambda_handler(event, context):
    text = 'Amazon Comprehend は、機械学習を使用してテキスト内の洞察と関係性を見つける自然言語処理 (NLP) サービスです。'
    language_code = 'ja'
    
    detect_key_phrases_response = detect_key_phrases(text, language_code)

    key_phrase_list = []
    for key_phrase in detect_key_phrases_response['KeyPhrases']:
        key_phrase_dict = {}
        key_phrase_dict['Text'] = key_phrase['Text']
        key_phrase_dict['Score'] = key_phrase['Score']
        key_phrase_list.append(key_phrase_dict)
    print(key_phrase_list)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }