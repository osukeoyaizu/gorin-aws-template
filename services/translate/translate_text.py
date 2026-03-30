import json
import boto3

translate = boto3.client('translate', region_name='ap-northeast-1')

# テキストを翻訳する
def translate_text(text, source_language_code, target_language_code):
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response


def lambda_handler(event, context):
    text = 'Translated text'
    source_language_code = 'en'
    target_language_code = 'ja'
    translate_text_response = translate_text(text, source_language_code, target_language_code)
    translated_text = translate_text_response['TranslatedText']
    print(translated_text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }