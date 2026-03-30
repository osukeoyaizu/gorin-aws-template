import boto3
import json
import uuid

lex_client = boto3.client('lexv2-runtime', region_name='ap-northeast-1')
sessionId = str(uuid.uuid4())

# インテントが完了するまで続ける
state = ''
while state != 'ConfirmIntent':

    result = lex_client.recognize_text(
            botId='M4LBRFHUMG',
            botAliasId='8FHPLKKME0',
            localeId='ja_JP',
            sessionId=sessionId,
            text=input('You: ')
            )
    #ボットの応答の表示
    print('Bot:', result['messages'][0]['content'])
    #会話の状態を取得
    state = result['sessionState']['dialogAction']['type']