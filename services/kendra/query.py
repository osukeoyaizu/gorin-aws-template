import json
import boto3

kendra = boto3.client("kendra", region_name="us-east-1")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

INDEX_ID = '3fddc561-bcd6-41ef-9b1b-40c9c520a61b'
MODEL_ID = 'amazon.nova-pro-v1:0'

# -----------------------------
# Bedrock（LLM）呼び出し
# -----------------------------
def invoke_model(prompt, model_id):
    request = {
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {
            "maxTokens": 256,
            "temperature": 0.2
        }
    }
    resp = bedrock.invoke_model(modelId=model_id, body=json.dumps(request))
    data = json.loads(resp["body"].read())
    return data["output"]["message"]["content"][0]["text"]

# -----------------------------
# Kendra Retrieve（意味検索）
# -----------------------------
def retrieve_from_kendra(query, index_id, page_size=10):
    resp = kendra.retrieve(
        QueryText=query,
        IndexId=index_id,
        PageSize=page_size
    )
    items = []
    for it in resp.get("ResultItems", []):
        items.append({
            "content": it.get("Content", ""),
            "uri": it.get("DocumentURI", ""),
            "score": it.get("ScoreAttributes", {})
        })
    return items

# -----------------------------
# Kendra Query（キーワード検索）
# -----------------------------
def query_from_kendra(query, index_id, page_size=10):
    resp = kendra.query(
        QueryText=query,
        IndexId=index_id,
        PageSize=page_size
    )
    items = []
    for it in resp.get("ResultItems", []):
        # Query は DocumentExcerpt.Text に抜粋が入る
        excerpt = (it.get("DocumentExcerpt") or {}).get("Text", "")
        items.append({
            "content": excerpt,
            "uri": it.get("DocumentURI", ""),
            "score": (it.get("ScoreAttributes") or {}),
            "title": ((it.get("DocumentTitle") or {}).get("Text"))
        })
    return items

# -----------------------------
# プロンプト生成
# -----------------------------
def build_prompt(question, contexts):
    context_text = "\n\n---\n\n".join([c["content"] for c in contexts]) or "(No related information)"
    return f"""You are a precise assistant. Answer only using the reference.
If the reference does not contain the answer, reply exactly with "Unknown".

[Question]
{question}

[Reference]
{context_text}

[Answer]
"""

# -----------------------------
# Lambda Handler
# -----------------------------
def lambda_handler(event, context):
    # TXTの書き方に合わせて「username」で尋ねる
    question = 'What product did username "rtanaka" purchase?'

    # 1) まず retrieve
    contexts = retrieve_from_kendra(question, INDEX_ID, page_size=10)

    # 2) 0件なら query にフォールバック（今回のログはここで当たっています）
    if not contexts:
        contexts = query_from_kendra('rtanaka', INDEX_ID, page_size=10)

    prompt = build_prompt(question, contexts)
    answer = invoke_model(prompt, MODEL_ID)

    return {
        "statusCode": 200,
        "body": json.dumps({"answer": answer, "sources": contexts}, ensure_ascii=False)
    }