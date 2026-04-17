## Cognitoの外部プロバイダーとして使用する場合
- Client作成
    - Client type:OpenID Connect
    - Client ID: 任意の名前
    - Client authentication: On
    - Valid redirect URIs:https://{CognitoのドメインURL}/oauth2/idpresponse
