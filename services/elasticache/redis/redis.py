import json
import os
import boto3
import redis

REGION_NAME = os.environ['REGION_NAME']
SECRETS_NAME = os.environ['SECRETS_NAME']

ttl = 20

# シークレット取得
def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=SECRETS_NAME
    )
    secret = get_secret_value_response['SecretString']
    return secret

    
# redis接続情報(転送中の暗号化有効)
def encrypted_connection_redis():
    secret = json.loads(get_secret())
    redis_host = secret['redis_host']
    redis_port = secret['redis_port']
    cache = redis.Redis(host=redis_host, port=redis_port, ssl=True, ssl_cert_reqs="none")
    return cache


# キャッシュデータ取得（サンプルデータを返す）
def check_cache(cache, key):
    response_data = cache.get(key)
    
    if response_data:
        print('Cache exists!')
        return json.loads(response_data)
    
    else:
        print('Cache not exists...')

        # ★ サンプルデータ（本来は API などから取得する想定）
        response_data = {
            "message": "This is sample data",
            "key": key,
            "value": 12345
        }

        # キャッシュを保存
        print('Cache setting')
        data = json.dumps(response_data)
        cache.set(key, data, ex=ttl)
        return response_data


# -----------------------------
# 🔥 ランキング処理
# -----------------------------

def update_score(cache, game_id, player_id, score):
    """スコアを登録（更新）"""
    cache.zadd(f"leaderboard:{game_id}", {player_id: score})


def get_rank(cache, game_id, player_id):
    """プレイヤーの順位を取得（1位始まり）"""
    rank = cache.zrevrank(f"leaderboard:{game_id}", player_id)
    return rank + 1 if rank is not None else None


def get_top_players(cache, game_id, top_n):
    """上位ランキングを取得"""
    results = cache.zrevrangebyscore(
        f"leaderboard:{game_id}",
        "+inf",
        "-inf",
        withscores=True,
        start=0,
        num=top_n
    )
    return [(player.decode(), score) for player, score in results]


# -----------------------------
# Lambda メイン処理
# -----------------------------

def lambda_handler(event, context):

    # redis接続
    cache = encrypted_connection_redis()

    # -----------------------------
    # ① キャッシュ処理
    # -----------------------------
    key = "sample_key"
    cache_data = check_cache(cache, key)

    # -----------------------------
    # ② ランキング処理（サンプル event）
    # -----------------------------
    game_id = event.get("gameId", "sample_game")
    player_id = event.get("playerId", "player_001")
    score = event.get("score", 1000)
    top_n = event.get("top", 5)

    # スコア更新
    update_score(cache, game_id, player_id, score)

    # 自分の順位
    rank = get_rank(cache, game_id, player_id)

    print(rank)

    # 上位ランキング
    top_players = get_top_players(cache, game_id, top_n)

    rank = 1
    results = []
    for item in top_players:
        result = {}
        result['rank'] = rank
        result['playerId'] = item[0]
        result['score'] = item[1]
        results.append(result)
        rank += 1
    print(results)

    # -----------------------------
    # レスポンス
    # -----------------------------
    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
