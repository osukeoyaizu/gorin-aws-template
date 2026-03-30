## 構築手順

**ポリシー作成**
```
aws iam create-policy --policy-name externalDNSPolicy --policy-document file://externalDNSPolicy.json
```

**ServiceAccount&IAMロールの作成**
```
eksctl create iamserviceaccount \
  --cluster <クラスター名> \
  --namespace kube-system \
  --name <サービスアカウント名> \
  --role-name <IAMロール名> \
  --override-existing-serviceaccounts \
  --attach-policy-arn <作成したIAMポリシーのARN> \
  --approve \
  --region <リージョンコード>
```

**デプロイする(deploymentとserviceは省略)**
```
kubectl apply -f externalDNSPod.yml
kubectl apply -f ingress.yml
```
