## 外部IdP連携
### keycloak
「Cognito」→「ユーザープール」→「ソーシャルプロバイダーと外部プロバイダー」→「アイデンティティプロバイダーを追加」

- OIDC
  - プロバイダー名:任意
  - クライアントID:Keycloakで作成したクライアントID
  - クライアントシークレット:KeycloakクライアントのSecret
  - 発行者URL:https://{Keycloakにアクセスするドメイン}/realms/{realms名}
  - 属性マッピング
    - ユーザープール属性:email
    - OpenID Connect属性:email


「Cognito」→「ユーザープール」→ 「アプリケーションクライアント」 → 「ログインページ」 → 「マネージドログインページを編集」
- 許可されているコールバックURL: https://{アプリケーションのドメイン}/callback
- デフォルトのリダイレクトURL: コールバックURLと一緒
- IDプロバイダー: 作成したもの
- OpenID Connectのスコープ: OpenID

### callback後の処理
ALB→Lambda(AssumeRole,S3からhtml取得,返却)
```python
import json
import os
import boto3
import base64
import urllib.parse
import urllib.request

sts = boto3.client("sts")

COGNITO_DOMAIN = os.environ["COGNITO_DOMAIN"] # us-east-xxxxxyyyyy.auth.{region}.amazoncognito.com
CLIENT_ID = os.environ["CLIENT_ID"] # アプリケーションクライアントID
REDIRECT_URI = os.environ["REDIRECT_URI"] # CognitoのクライアントのコールバックURLと完全一致

ROLE_MAP = {
    "user01@example.com": "arn:aws:iam::140083316867:role/user01",
    "user02@example.com": "arn:aws:iam::140083316867:role/user02",
}

# ---- helper ----


def exchange_code_for_token(code):
    url = f"https://{COGNITO_DOMAIN}/oauth2/token"

    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print("Token endpoint error:", error_body)
        raise


def decode_jwt(token):
    """
    JWT を base64 decode(署名検証なし)
    """
    payload = token.split(".")[1]
    padding = "=" * (-len(payload) % 4)
    decoded = base64.urlsafe_b64decode(payload + padding)
    return json.loads(decoded)

def response(status, body):
    return {
        "statusCode": status,
        "body": body
    }

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))
    # ① code を取得
    params = event.get("queryStringParameters") or {}
    code = params.get("code")

    if not code:
        return response(400, "missing code")

    # ② code → token 交換
    token = exchange_code_for_token(code)

    id_token = token.get("id_token")
    if not id_token:
        return response(500, "id_token not returned")

    # ③ id_token を decode（署名検証なし）
    claims = decode_jwt(id_token)
    print(claims)

    email = claims.get("email")
    sub = claims.get("sub")

    if email not in ROLE_MAP:
        return response(403, "user not allowed")

    # ④ ユーザー別 IAM ロール Assume
    assumed = sts.assume_role(
        RoleArn=ROLE_MAP[email],
        RoleSessionName=f"user-{sub}",
        DurationSeconds=3600
    )

    credential = assumed["Credentials"]

    session = boto3.Session(
        aws_access_key_id=credential['AccessKeyId'],
        aws_secret_access_key=credential['SecretAccessKey'],
        aws_session_token=credential['SessionToken'],
    )

    s3 = session.client('s3')


    # ④ index.html を取得
    obj = s3.get_object(Bucket='sample-bucket', Key='index.html')
    html_body = obj["Body"].read().decode("utf-8")

    # ⑤ ALB 用レスポンスとして返す
    return {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": html_body
    }


```