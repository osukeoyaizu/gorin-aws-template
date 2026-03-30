## Kendra+BedrockのRAG構築
### Kendraでインデックス作成
インデックスを作成し、データソースとして正しいS3バケット、パスを設定する

※同期する

### Lambda関数
```
import json
import os
import boto3

kendra = boto3.client("kendra", region_name="us-east-1")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

INDEX_ID = os.environ["INDEX_ID"]
MODEL_ID = os.environ["MODEL_ID"]

# -----------------------------
# Bedrock（LLM）呼び出し
# -----------------------------
def invoke_model(prompt, model_id):
    request = {
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {
            "maxTokens": 512,
            "temperature": 0.5
        }
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(request)
    )

    model_response = json.loads(response["body"].read())
    return model_response["output"]["message"]["content"][0]["text"]


# -----------------------------
# Kendra Retrieve
# -----------------------------
def retrieve_from_kendra(query, index_id, language_code):
    response = kendra.retrieve(
        QueryText=query,
        IndexId=index_id,
        AttributeFilter={
            "EqualsTo": {
                "Key": "_language_code",
                "Value": {"StringValue": language_code},
            },
        },
    )

    print(response)

    items = []
    for item in response.get("ResultItems", []):
        items.append({
            "content": item.get("Content", ""),
            "uri": item.get("DocumentURI", "")
        })

    return items


# -----------------------------
# プロンプト生成
# -----------------------------
def build_prompt(question, contexts):
    context_text = "\n\n---\n\n".join([c["content"] for c in contexts]) or "（関連情報なし）"

    return f"""
以下の参考情報に基づいて質問に答えてください。

[質問]
{question}

[参考情報]
{context_text}

回答:
"""


# -----------------------------
# Lambda Handler
# -----------------------------
def lambda_handler(event, context):
    body = json.loads(event["body"])
    question = body["prompt"]

    # 1. Kendra Retrieve
    language_code = 'ja' # ドキュメント（検索対象コンテンツ）の言語
    retrieved = retrieve_from_kendra(question, INDEX_ID)

    # 2. プロンプト生成
    prompt = build_prompt(question, retrieved)

    # 3. Bedrock LLM 呼び出し
    answer = invoke_model(prompt, MODEL_ID)

    # 4. 回答 + 参照元を返す
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "answer": answer,
                "sources": retrieved
            },
            ensure_ascii=False
        )
    }

```
