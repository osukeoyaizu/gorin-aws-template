## keycloak
https://qiita.com/gaichi/items/4e58d1d1c3ad4a024ffd

### AWSのSAML用メタデータ取得
- https://signin.aws.amazon.com/static/saml-metadata.xml
    - ローカルに保存

### keycloak側の設定
![alt text](images/image.png)

- 保存したsaml-metadata.xmlを使用

![alt text](images/image-1.png)

- Root URL: https://<keycloakのホスト名>
- Home URL: /realms/master/protocol/saml/clients/aws-saml
- IDP-Initiated SSO URL name: aws-saml

![alt text](images/image-2.png)

- ローカルに保存

![alt text](images/image-3.png)


### AWS IAM設定

![alt text](images/image-4.png)
- ロール作成
    - ロールとプロバイダのARNをコピー

![alt text](images/image-5.png)


### keycloak側の設定(2)
- client(urn:amazon:webservices)にロール作成
    - 「ロールのARN,IDプロバイダのARN」

![alt text](images/image-6.png)

- クライアントスコープ削除

![alt text](images/image-7.png)

- urn:amazon:webservices-dedicatedの「RoleSessionName」「Role」を削除

![alt text](images/image-8.png)

- mapper作成

![alt text](images/image-9.png)
- Session Role
    - Mapper type: Role list
    - Name: Session Role
    - Role attribute name: https://aws.amazon.com/SAML/Attributes/Role
    - Friendly Name: Session Role
    - SAML Attribute NameFormat: Basic
    - Single Role Attribute: On

![alt text](images/image-10.png)

- Session Role
    - Mapper type: User Property
    - Name: Session Name
    - Property: usernmae
    - Role attribute name: https://aws.amazon.com/SAML/Attributes/RoleSessionName
    - Friendly Name: Session Name
    - SAML Attribute NameFormat: Basic

![alt text](images/image-11.png)

- Full scope allowedをOffにする

![alt text](images/image-12.png)

- GoupとUserを作成し、グループに参加させる

![alt text](images/image-13.png)

- グループにロールをマッピングする

![alt text](images/image-14.png)

### 確認
- https://<keycloakホスト名>/realms/master/protocol/saml/clients/aws-saml 
    - 作成したユーザーでログインする → マッピングしたロールでログインされる 

## github
### 手順
https://zenn.dev/kou_pg_0131/articles/gh-actions-oidc-aws




/realms/platform/protocol/saml/clients/aws-saml