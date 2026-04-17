## トークン取得方法
### 認可コード取得
ログインページからユーザー名、パスワードを使用してログインする

ログイン後、ブラウザが次のような URL にリダイレクトされる
```
https://xxxxxyyyyy.cloudfront.net/?code={AUTHORIZATION_CODE}
```

### トークン取得コマンド
```
curl -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id={YOUR_CLIENT_ID}" \
  -d "code={AUTHORIZATION_CODE}" \
  -d "redirect_uri=https://xxxxxyyyyy.cloudfront.net" \
  https://{YOUR_DOMAIN}.auth.{YOUR_REGION}.amazoncognito.com/oauth2/token \
  | jq .
```

## MFA
- ユーザープールでMFA有効化
- アクセストークン取得
- SecretCode取得
```
aws cognito-idp associate-software-token \
  --access-token <ACCESS_TOKEN>
```
- Authenticatorアプリで出力されたSecretCodeを入力する
- 確認コマンド
```
aws cognito-idp verify-software-token \
  --access-token <ACCESS_TOKEN> \
  --user-code <アプリの6桁コード> \
  --friendly-device-name "MyPhone"
```
- ユーザーでMFA有効化
```
aws cognito-idp set-user-mfa-preference \
  --access-token <ACCESS_TOKEN> \
  --software-token-mfa-settings Enabled=true,PreferredMfa=true
```



## ユーザープール移行
- 旧アプリケーションクライアントで[ALLOW_ADMIN_USER_PASSWORD_AUTH]にチェックをつける
- 新ユーザープールで[ユーザーを移行Lambdaトリガー]を設定する
- Lambda関数
```python
import boto3
import os
client = boto3.client("cognito-idp")
def lambda_handler(event, context):
    username = event["userName"]
    password = event["request"]["password"]
    try:
        auth_result = client.admin_initiate_auth(
            UserPoolId=os.environ["OLD_USER_POOL_ID"],
            ClientId=os.environ["OLD_CLIENT_ID"],
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )
        # 認証成功 → 属性取得
        user = client.admin_get_user(
            UserPoolId=os.environ["OLD_USER_POOL_ID"],
            Username=username
        )
        attributes = {attr["Name"]: attr["Value"] for attr in user["UserAttributes"]}
        # 属性の移行（必要なものだけ抽出も可）
        event["response"]["userAttributes"] = {
            "email": attributes.get("email", ""),
            "email_verified": "true",
            # "custom:your_attr": attributes.get("custom:your_attr", "")
        }
        event["response"]["finalUserStatus"] = "CONFIRMED"
        event["response"]["messageAction"] = "SUPPRESS"
        event["response"]["forceAliasCreation"] = False
    except client.exceptions.NotAuthorizedException:
        raise Exception("認証失敗：パスワードが正しくありません")
    except client.exceptions.UserNotFoundException:
        raise Exception("認証失敗：旧ユーザープールにユーザーが存在しません")
    
return event
```

## ALB
- ACM作成
- Route53でエイリアスレコード作成
- ユーザープール作成
  - 従来のアプリケーション(クライアントシークレットが必要)
  - コールバックURL
    - https://<DNS名>/oauth2/idpresponse
- ALBで443リスナーでCognitoの設定する

## OpenSearch
- Cognito設定
  - ユーザープール作成
  - IDプール作成
    - IDプールのIAMロールに必要な権限
    ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "Statement1",
                  "Effect": "Allow",
                  "Action": [
                      "es:ESHttpGet"
                  ],
                  "Resource": [
                      "*"
                  ]
              }
          ]
    }
    ```
  - OpenSearch設定後にマネージドログインのスタイルを選択する
- OpenSearch設定
  - きめ細かなアクセスコントロールのチェック外す
  - Cognito認証有効化
  - リソースポリシー
  ```
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "{IDプールのIAMロールARN}"
        },
        "Action": "es:*",
        "Resource": "arn:aws:es:{リージョン}:{アカウントID}:domain/{ドメイン名}/*"
      }
    ]
  }
  ```
