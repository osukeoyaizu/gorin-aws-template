## fargateでポッドのログ記録
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/fargate-logging.html

###  aws-observability-namespace.yamlという名前のファイルに保存
```
kind: Namespace
apiVersion: v1
metadata:
  name: aws-observability
  labels:
    aws-observability: enabled
```
### 名前空間を作成します。
```
kubectl apply -f aws-observability-namespace.yaml
```


### aws-logging-cloudwatch-configmap.yaml という名前のファイルに保存
```
kind: ConfigMap
apiVersion: v1
metadata:
  name: aws-logging
  namespace: aws-observability
data:
  flb_log_cw: "false"  # Set to true to ship Fluent Bit process logs to CloudWatch.
  filters.conf: |
    [FILTER]
        Name parser
        Match *
        Key_name log
        Parser crio
    [FILTER]
        Name kubernetes
        Match kube.*
        Merge_Log On
        Keep_Log Off
        Buffer_Size 0
        Kube_Meta_Cache_TTL 300s
  output.conf: |
    [OUTPUT]
        Name cloudwatch_logs
        Match   kube.*
        region <リージョンコード>
        log_group_name <保存先ロググループ名>
        log_stream_prefix from-fluent-bit-
        log_retention_days 60
        auto_create_group true
  parsers.conf: |
    [PARSER]
        Name crio
        Format Regex
        Regex ^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>P|F) (?<log>.*)$
        Time_Key    time
        Time_Format %Y-%m-%dT%H:%M:%S.%L%z
```

### ConfigMapを作成
```
kubectl apply -f aws-logging-cloudwatch-configmap.yaml
```

### Fargate Pod 実行ロールに対するアクセス許可を設定
```
curl -O https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/cloudwatchlogs/permissions.json
aws iam create-policy --policy-name eks-fargate-logging-policy --policy-document file://permissions.json
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::<アカウントID>:policy/eks-fargate-logging-policy \
  --role-name <AmazonEKSFargatePodExecutionRole>
                  
```

**Podを再起動する必要がある**
