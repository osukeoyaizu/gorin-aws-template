## AWS Load Balancer Controller のセットアップ
### OIDC プロバイダーの作成
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/enable-iam-roles-for-service-accounts.html
```
cluster_name=<クラスター名>
region_name=<リージョン名>
```
```
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo $oidc_id
eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve --region $region_name
```

### helmのインストール
https://helm.sh/docs/intro/install/
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Helm で AWS Load Balancer Controllerのインストール
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/lbc-helm.html

**ポリシーをダウンロード**
```
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.11.0/docs/install/iam_policy.json
```

**IAMポリシーを作成**
```
aws iam create-policy \
    --policy-name <ポリシー名> \
    --policy-document file://iam_policy.json
```

**ロールにポリシーをアタッチする**
```
eksctl create iamserviceaccount \
  --cluster=$cluster_name \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name <ロール名> \
  --attach-policy-arn=arn:aws:iam::<アカウントID>:policy/<ポリシー名> \
  --approve \
  --region $region_name
```

**eks-charts Helm チャートリポジトリを追加**
```
helm repo add eks https://aws.github.io/eks-charts
```
**ローカルリポジトリを更新して、最新のグラフがあることを確認する**
```
helm repo update eks
```

**AWS Load Balancer Controller をインストール**
```
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=$cluster_name \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=$region_name \
  --set vpcId=<VPC ID>
```
**CRDs をインストール**
```
wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
kubectl apply -f crds.yaml
```

**コントローラがインストールされていることを確認**
```
kubectl get deployment -n kube-system aws-load-balancer-controller
```

### デプロイする

**①プライベートサブネットとパブリックサブネットにタグ付けをする**

| サブネット | キー | 値 |
| ---- | ---- | ---- |
| public | kubernetes.io/role/elb | 1 |
| private | kubernetes.io/role/internal-elb | 1 |

**②Fargate プロファイルを作成する(Fargateにデプロイする場合)**
```
eksctl create fargateprofile \
    --cluster $cluster_name \
    --region $region_name \
    --name <プロファイル名> \
    --namespace <名前空間名>
```

**③マニフェストをクラスターに適用**
```
kubectl apply -f <マニュフェストファイル>
```
