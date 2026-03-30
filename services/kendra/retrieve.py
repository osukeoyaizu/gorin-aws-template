import json
import os
import boto3

INDEX_ID = os.environ['INDEX_ID']
kendra = boto3.client("kendra", region_name="us-east-1")

def get_retrieval_result(query_text, language_code, index_id):
    """
    Kendraに質問文を投げて検索結果を取得する

    Args:
        query_text (str): 質問文
        index_id (str): Kendra インデックス ID

    Returns:
        list: 検索結果のリスト
    """
    # Kendra に質問文を投げて検索結果を取得
    response = kendra.retrieve(
        QueryText=query_text,
        IndexId=index_id,
        AttributeFilter={
            "EqualsTo": {
                "Key": "_language_code",
                "Value": {"StringValue": language_code},
            },
        },
    )

    # 検索結果から上位5つを抽出
    results = response["ResultItems"][:5] if response["ResultItems"] else []

    # 検索結果の中から文章とURIのみを抽出
    extracted_results = []
    for item in results:
        content = item.get("Content")
        document_uri = item.get("DocumentURI")

        extracted_results.append(
            {
                "Content": content,
                "DocumentURI": document_uri,
            }
        )
    return extracted_results


def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_prompt = body['prompt']
    language_code = 'en'

    # Kendra に質問文を投げて検索結果を取得
    kendra_response = get_retrieval_result(user_prompt, language_code, INDEX_ID)

    print(kendra_response)

    return {
        "statusCode": 200,
        "body": json.dumps({"answer":kendra_response}, ensure_ascii=False),
    }
