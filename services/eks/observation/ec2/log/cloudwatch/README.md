## EC2でポッドのログ記録
https://repost.aws/ja/knowledge-center/cloudwatch-stream-container-logs-eks

###  amazon-cloudwatch という名前の名前空間を作成
```
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml
```
### ConfigMap作成
```
ClusterName=my-cluster-name
RegionName=my-cluster-region
FluentBitHttpPort='2020'
FluentBitReadFromHead='Off'
[[ ${FluentBitReadFromHead} = 'On' ]] && FluentBitReadFromTail='Off'|| FluentBitReadFromTail='On'
[[ -z ${FluentBitHttpPort} ]] && FluentBitHttpServer='Off' || FluentBitHttpServer='On'
kubectl create configmap fluent-bit-cluster-info \
--from-literal=cluster.name=${ClusterName} \
--from-literal=http.server=${FluentBitHttpServer} \
--from-literal=http.port=${FluentBitHttpPort} \
--from-literal=read.head=${FluentBitReadFromHead} \
--from-literal=read.tail=${FluentBitReadFromTail} \
--from-literal=logs.region=${RegionName} -n amazon-cloudwatch
```


### DaemonSetマニフェスト取得
```
curl -O https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/fluent-bit/fluent-bit.yaml
```

### マニフェスト適用
```
mv fluent-bit.yaml fluent-bit-cloudwatch.yaml
kubectl apply -f fluent-bit-cloudwatch.yaml
```

**※エラーが発生する際は一度削除してからapplyする**

### サービスアカウント設定
```
eksctl create iamserviceaccount \
    --name fluent-bit \
    --namespace amazon-cloudwatch \
    --cluster $ClusterName \
    --attach-policy-arn "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy" \
    --approve \
    --override-existing-serviceaccounts
```

### DaemonSet再起動
```
kubectl rollout restart daemonset fluent-bit -n amazon-cloudwatch
```

**Podを再起動する必要がある**
