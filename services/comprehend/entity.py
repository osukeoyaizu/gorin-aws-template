import json
import boto3

comprehend = boto3.client('comprehend', region_name='ap-northeast-1')


def detect_entities(text, language_code):
    response = comprehend.detect_entities(Text=text, LanguageCode=language_code)
    return response


def lambda_handler(event, context):
    text = 'Amazon Comprehend は、機械学習を使用してテキスト内の洞察と関係性を見つける自然言語処理 (NLP) サービスです。'
    language_code = 'ja'

    detect_entities_response = detect_entities(text, language_code)
    
    entity_list = []
    for entity in detect_entities_response['Entities']:
        entity_dict = {}
        entity_dict['Text'] = entity['Text']
        entity_dict['Type'] = entity['Type']
        entity_dict['Score'] = entity['Score']
        entity_list.append(entity_dict)
    print(entity_list)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
