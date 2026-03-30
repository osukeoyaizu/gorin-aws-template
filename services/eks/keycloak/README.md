## 設定手順
- PostgreSQLをRDSで起動する
- DockerfileをECRにプッシュする
- deployment.yamlの環境変数を設定する
- ingressで公開する
- https://{ホスト名}/adminにアクセスする　→ adminユーザーが作られていない
- keycloakコンテナに入る
```
kubectl exec -it -n {名前空間} {Pod名} -- /bin/bash
``` 
- コマンド実行
```
/opt/keycloak/bin/kc.sh bootstrap-admin user
```