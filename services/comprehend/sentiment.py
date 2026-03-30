import json
import boto3

comprehend = boto3.client('comprehend', region_name='ap-northeast-1')

# 感情検出
def detect_sentiment(text, language_code):
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response


def lambda_handler(event, context):
    # 編集内容
    text = 'thankyou'
    language_code = 'en'

    # 感情検出
    detect_sentiment_response = detect_sentiment(text, language_code)
    sentiment = detect_sentiment_response['Sentiment']

    print(detect_sentiment_response['Sentiment'])
    print(detect_sentiment_response['SentimentScore'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }