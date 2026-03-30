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
