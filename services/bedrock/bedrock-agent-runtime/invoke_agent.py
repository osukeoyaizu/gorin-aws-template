import json
import boto3
import os

AGENT_ID = os.environ['AGENT_ID']
AGENT_ALIAS_ID = os.environ['AGENT_ALIAS_ID']

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")


def invoke_agent(prompt, session_id):
    response = bedrock_agent_runtime.invoke_agent(
        inputText=prompt,
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        enableTrace=False
    )

    event_stream = response['completion']
    answer = ''
    for event in event_stream:        
        if 'chunk' in event:
            answer = event['chunk']['bytes'].decode("utf-8")
    return answer


def lambda_handler(event, context):
    body = json.loads(event['body'])
    prompt = body['prompt']
    session_id = body['session_id']
    invoke_agent_response = invoke_agent(prompt, session_id)

    return {
        'statusCode': 200,
        'body': json.dumps({"answer":invoke_agent_response}, ensure_ascii=False)
    }
