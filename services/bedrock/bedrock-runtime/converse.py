import json
import boto3

bedrock_runtime_client = boto3.client('bedrock-runtime', region_name='ap-northeast-1')

def converse(prompt, system_prompt, modelId):
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    inferenceConfig = {
        "temperature": 0.1,
        "topP": 0.9,
        "maxTokens": 500,
        "stopSequences":[]
    }
    response = bedrock_runtime_client.converse(
        modelId=modelId ,
        messages=messages,
	    system=[
	        { "text": system_prompt }
        ],
        inferenceConfig=inferenceConfig
    )
    return response


def lambda_handler(event, context):
    prompt = "AWSについて教えてください。"
    modelId = "amazon.nova-lite-v1:0"
    system_prompt = "関西弁であらゆるリクエストに答えてください。"

    invoke_model_response = converse(prompt, system_prompt, modelId)
    response_text = invoke_model_response["output"]["message"]["content"][0]["text"]
    print(response_text)

    return {
        'statusCode': 200,
        'body': json.dumps({'response': response_text})
    }