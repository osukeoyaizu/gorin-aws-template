import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

boto3_session = boto3.session.Session()
region = boto3_session.region_name
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

model_id = 'amazon.nova-lite-v1:0'
model_arn = f'arn:aws:bedrock:{region}::foundation-model/{model_id}'
kbId = os.environ['KNOELEDGEBASE_ID']
grId = os.environ['GUARDRAILD_ID']

def retrieveAndGenerate(input_text):
    response = bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': input_text
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'generationConfiguration': {
                    'guardrailConfiguration': {
                        'guardrailId': grId,
                        'guardrailVersion': 'DRAFT'
                    }
                },
                'knowledgeBaseId': kbId,
                'modelArn': model_arn
                },
            'type': 'KNOWLEDGE_BASE'
        }
    )
    return response

def lambda_handler(event, context):
    body = json.loads(event['body'])
    input_text = body['userInput']

    response = retrieveAndGenerate(input_text)
    response = response['output']['text']
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps({'response': response}, ensure_ascii=False)
    }




