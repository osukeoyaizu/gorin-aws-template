import json
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def invoke_model(prompt, modelId):
    if "mistral" in modelId:
        native_request = {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 512,
            "temperature": 0.5,
        }
    elif "titan" in modelId:
        native_request = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
            },
        }
    elif "nova" in modelId:
        native_request = {
            "messages": [
                {"role": "user", "content": [{"text": prompt}]}
            ],
            "inferenceConfig": {
                "maxTokens": 512,
                "temperature": 0.5,
            }
        }
    elif "claude" in modelId:
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": 512,
            "temperature": 0.5,
        }
    else:
        raise ValueError(f"Unsupported modelId: {modelId}")

    response = bedrock.invoke_model(
        modelId=modelId,
        body=json.dumps(native_request),
        # guardrailIdentifier='<GUARDRAILD_ID>',
        # guardrailVersion='DRAFT'
    )
    model_response = json.loads(response["body"].read())

    if "mistral" in modelId:
        response_text = model_response["choices"][0]["message"]["content"]
    elif "nova" in modelId:
        response_text = model_response["output"]["message"]["content"][0]["text"]
    elif "titan" in modelId:
        response_text = model_response["results"][0]["outputText"]
    elif "claude" in modelId:
        response_text = model_response["content"][0]["text"]
    else:
        response_text = "Unsupported model response format"

    return response_text



def lambda_handler(event, context):
    text = '地球温暖化は、主に人間の活動によって引き起こされており、温室効果ガスの排出が増加しています。この現象は、気候変動や極端な気象を引き起こし、生態系に深刻な影響を与えています。'
    prompt = f"次の文章を英語にしてください。: {text}"

    modelId = "amazon.titan-text-express-v1"

    # modelId = "amazon.nova-lite-v1:0"

    # modelId = "mistral.mistral-large-3-675b-instruct"

    # modelId = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

    response_text = invoke_model(prompt, modelId)

    return {
        'statusCode': 200,
        'body': json.dumps({'response': response_text}, ensure_ascii=False)
    }
