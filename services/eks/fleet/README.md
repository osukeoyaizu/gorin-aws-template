## 前提条件
- HubクラスターARN:arn:aws:eks:us-east-1:{account-id}:cluster/oyaizu-eks-hub

- SpokeクラスターARN:arn:aws:eks:us-east-1:{account-id}:cluster/oyaizu-eks-spoke-prod

- リポジトリURL:https://git-codecommit.us-east-1.amazonaws.com/v1/repos/oyaizu-eks


- OIDC プロバイダーの作成

- helmのインストール

- ArgoCD Capabilitiesインストール
    - アクセスエントリ設定

## サービスアカウント用のロール作成
信頼ポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "<OIDC_PROVIDER_ARN>"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.us-east-1.amazonaws.com/id/<OIDC_PROVIDER_ID>:aud": "sts.amazonaws.com",
                    "oidc.eks.us-east-1.amazonaws.com/id/<OIDC_PROVIDER_ID>:sub": "system:serviceaccount:fleet-system:external-secrets"
                }
            }
        }
    ]
}
```
権限にkms,secretsmanagerへのアクセス権をつける

## SecretsManager作成
「/fleet/members/<spokeのクラスター名>/registration」という名前で作成する必要がある
```
{
  "clusterName": "oyaizu-eks-spoke-prod",
  "clusterArn": "arn:aws:eks:us-east-1:140083316867:cluster/oyaizu-eks-spoke-prod",
  "clusterEndpoint": "https://1C47532D17B9042C6EF1BD2E25F40992.gr7.us-east-1.eks.amazonaws.com",
  "certificateAuthorityData": "LS0tLS1CRU..."
}
```

## ServiceAccount作成
```
namespace/fleet-system created
kubectl apply -f eks/serviceaccount/serviceaccount.yaml
```

## Secretデプロイ
```
kubectl apply -f eks/secrets/
```

## Applicationデプロイ
```
kubectl apply -f eks/applicaions/application-eso-helm.yaml
kubectl apply -f eks/applicaions/application-fleet-hub.yaml
```


## ApplicationSetデプロイ
```
kubectl apply -f eks/applicationsets/fleet-hub-controller.yaml
```

