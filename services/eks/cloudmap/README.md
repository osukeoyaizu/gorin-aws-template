## 前提条件

### frontendコンテナとbackendコンテナが作成済
frontendはALBで公開済

### CoreDNSアドオンを追加しておく

### OIDC プロバイダーの作成
※Frontend、Backendクラスターそれぞれに用意する

### ServiceAccountに紐づけるIAMロールを作成する
※Frontend、Backendクラスターそれぞれに用意する

ポリシー:AWSCloudMapFullAccess

信頼ポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "{OIDCのIDプロバイダのARN}"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.{REGION}.amazonaws.com/id/{プロバイダのID}:sub": "system:serviceaccount:cloud-map-mcs-system:cloud-map-mcs-controller-manager"
                }
            }
        }
    ]
}
```

### VPC間で通信できるようにしておく
VPCピアリングやTransit Gatewayを使用


## 設定方法
※Frontend、Backendクラスターそれぞれで実行する
### Cloud Map MCS Controller のインストール
```
kubectl apply -k "github.com/aws/aws-cloud-map-mcs-controller-for-k8s/config/controller_install_release"
```

### ServiceAccount に IAM ロールを紐づける
```
kubectl annotate serviceaccount \
  -n cloud-map-mcs-system cloud-map-mcs-controller-manager \
  eks.amazonaws.com/role-arn={ServiceAccount用ロールARN} \
  --overwrite
```

### AWS_REGION を正しく設定
``` 
kubectl -n cloud-map-mcs-system edit configmap cloud-map-mcs-aws-config
```

### CoreDNS の設定変更
```
kubectl edit configmap coredns -n kube-system
```

#### 追加内容(readyの上に追加)
```
multicluster clusterset.local
```

### CoreDNS の RBAC 権限を拡張
```
kubectl edit clusterrole system:coredns
```

#### 追加内容
```
- apiGroups:
  - discovery.k8s.io
  resources:
  - endpointslices
  verbs:
  - list
  - watch
  - get
  - create
  - update

- apiGroups:
  - multicluster.x-k8s.io
  resources:
  - serviceimports
  verbs:
  - create
  - get
  - list
  - patch
  - update
  - watch

- apiGroups:
  - multicluster.x-k8s.io
  resources:
  - serviceexports
  verbs:
  - get
  - list
  - patch
  - update
  - watch
```


##　CoreDNS イメージを MCS 対応版に更新
```
kubectl set image --namespace kube-system deployment.apps/coredns \
    coredns=ghcr.io/aws/aws-cloud-map-mcs-controller-for-k8s/coredns-multicluster/coredns:v1.8.6
```

##　Backend用 Namespaceを作成
```
kubectl create namespace backend-namespace
```

### ClusterPropertyを作成する
frontend/cluster-property.yaml

backend/cluster-property.yaml

を作成してapplyする

### Backend クラスターのみ：ServiceExport を作成
**※Backend用クラスターでのみ実行する**
service-export.yamlを作成する
```
apiVersion: multicluster.x-k8s.io/v1alpha1
kind: ServiceExport
metadata:
  name: backend-service
  namespace: backend-namespace
```

### cloud-map-mcs-controller-managerを再起動する
```
kubectl -n cloud-map-mcs-system rollout restart deploy/cloud-map-mcs-controller-manager
kubectl -n cloud-map-mcs-system rollout status  deploy/cloud-map-mcs-controller-manager
```

### ログ確認
```
kubectl -n cloud-map-mcs-system logs deploy/cloud-map-mcs-controller-manager -c manager --tail=200
```


### 検証方法

#### frontend 側にテスト Pod を作成
```
kubectl run test \
  -n frontend-namespace \
  --image=busybox:latest \
  --command -- sleep 3600
```

#### Pod に入る
```
kubectl -n frontend-namespace exec -it test -- sh
```

#### backend-service の名前解決を確認
```
nslookup backend-service.backend-namespace.svc.clusterset.local
```
