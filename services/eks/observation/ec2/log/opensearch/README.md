## EC2でポッドのログ記録

###  amazon-opensearch という名前の名前空間を作成
```
kubectl create namespace amazon-opensearch
```
### ConfigMap作成
```
ClusterName=my-cluster-name
RegionName=my-cluster-region
FluentBitHttpPort='2020'
FluentBitReadFromHead='Off'
[[ ${FluentBitReadFromHead} = 'On' ]] && FluentBitReadFromTail='Off'|| FluentBitReadFromTail='On'
[[ -z ${FluentBitHttpPort} ]] && FluentBitHttpServer='Off' || FluentBitHttpServer='On'
kubectl create configmap fluent-bit-opensearch-cluster-info \
--from-literal=cluster.name=${ClusterName} \
--from-literal=http.server=${FluentBitHttpServer} \
--from-literal=http.port=${FluentBitHttpPort} \
--from-literal=read.head=${FluentBitReadFromHead} \
--from-literal=read.tail=${FluentBitReadFromTail} \
--from-literal=logs.region=${RegionName} -n amazon-opensearch
```


### git上のfluent-bit-opensearch.yamlをダウンロードする


### fluent-bit-opensearch.yamlのOUTPUT部分を変更
```
    [OUTPUT]
        Name  es  
        Match *
        Host  search-oyaizu-4cfsypft4ajomgeykqu5d4pnqu.aos.ap-northeast-1.on.aws
        Port  443 
        Index oyaizu-eks-ec2-logs
        Type  _doc
        AWS_Auth On
        AWS_Region ap-northeast-1
        tls   On
        Suppress_Type_Name On
```

### マニフェスト適用
```
kubectl apply -f fluent-bit-opensearch.yaml
```

**※エラーが発生する際は一度削除してからapplyする**


### fluent-bit-opensearch-policy.json作成
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "es:ESHttpPut",
        "es:ESHttpPost",
        "es:ESHttpGet"
      ],
      "Resource": "*"
    }
  ]
}
```

### IAM ポリシーを作成
```
aws iam create-policy \
  --policy-name FluentBitOpenSearchPolicy \
  --policy-document file://fluent-bit-opensearch-policy.json
```

### サービスアカウント設定
```
eksctl create iamserviceaccount \
    --name fluent-bit-opensearch \
    --namespace amazon-opensearch \
    --cluster $ClusterName \
    --attach-policy-arn "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy" \
    --approve \
    --override-existing-serviceaccounts
```

###  OpenSearchでサービスアカウントのロールからのアクセスを許可する
```
curl -sS -u "{OpenSearchユーザー名}:{OpenSearchパスワード}" \
    -X PATCH \
    https://{ドメインエンドポイント}/_opendistro/_security/api/rolesmapping/all_access\?pretty \
    -H 'Content-Type: application/json' \
    -d'
[
  {
    "op": "add", "path": "/backend_roles", "value": ["{サービスアカウントのロールARN}"]
  }
]'
```

### 作成されたロールにlogsへの権限もアタッチしておく

### DaemonSet再起動
```
kubectl rollout restart daemonset fluent-bit-opensearch -n amazon-opensearch
```

**Podを再起動する必要がある**
