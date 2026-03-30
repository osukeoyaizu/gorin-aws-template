## fargateでポッドのログ記録
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/fargate-logging.html

###  OpenSearchでポッド実行ロールからのアクセスを許可する
```
curl -sS -u "{OpenSearchユーザー名}:{OpenSearchパスワード}" \
    -X PATCH \
    https://{ドメインエンドポイント}/_opendistro/_security/api/rolesmapping/all_access\?pretty \
    -H 'Content-Type: application/json' \
    -d'
[
  {
    "op": "add", "path": "/backend_roles", "value": ["{ポッド実行ロールARN}"]
  }
]'
```

### aws-logging-opensearch-configmap.yaml という名前のファイルに保存
```
kind: ConfigMap
apiVersion: v1
metadata:
  name: aws-logging
  namespace: aws-observability
data:
  output.conf: |
    [OUTPUT]
      Name  es
      Match *
      Host  {ドメインエンドポイント(https://なし)}
      Port  443
      Index {インデックス名}
      Type  _doc
      AWS_Auth On
      AWS_Region ap-northeast-1
      tls   On
      Suppress_Type_Name On
```

### ConfigMapを作成
```
kubectl apply -f aws-logging-opensearch-configmap.yaml
```

**Podを再起動する必要がある**
