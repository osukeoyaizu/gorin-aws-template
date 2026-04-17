## Batch on EKS
### 前提条件
- EKSクラスター作成
    - クラスターアクセス: EKS API と ConfigMap
    - OIDCプロバイダー作成

### 名前空間作成
```
kubectl create namespace {名前空間}
```

### サービスアカウント作成
```
eksctl create iamserviceaccount \
  --cluster={クラスター名} \
  --namespace={名前空間} \
  --name={サービスアカウント名} \
  --role-name <ロール名> \
  --attach-policy-arn=arn:aws:iam::<アカウントID>:policy/<ポリシー名> \
  --approve \
  --region {リージョン}
```

### インスタンスロール作成
「EKSクラスター」→「コンピューティング」→「ノードグループを追加」→「推奨ロールを作成」から作成するのがおすすめ
- AmazonEC2ContainerRegistryReadOnly
- AmazonEKS_CNI_Policy
- AmazonEKSWorkerNodePolicy
- AmazonElasticContainerRegistryPublicReadOnly

### configmap.yaml
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::140083316867:role/oyaizu-batch-instance-role
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes

    - rolearn: arn:aws:iam::140083316867:role/AWSServiceRoleForBatch
      username: aws-batch
      groups:
        - system:masters
```

### ジョブ環境作成
インスタンスロール:作成してあるもの

### ジョブキュー作成
作成した環境を指定する

### ジョブ定義作成
サービスアカウント、名前空間を指定する


### 確認
ジョブを送信するとノードインスタンスが作成され、実行される

### Runnableから動かない
- インスタンスがノードに登録されていない
    - インスタンスロールの権限
    - インスタンスとクラスターが相互通信(セキュリティグループ)
- インスタンスサイズが小さい
    - 環境のインスタンスサイズを修正する