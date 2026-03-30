## Container Insights EKS Fargate
https://aws-otel.github.io/docs/getting-started/container-insights/eks-fargate

###  ADOT Collector を EKS Fargate にデプロイする
```
##!/bin/bash
CLUSTER_NAME=YOUR-EKS-CLUSTER-NAME
REGION=YOUR-EKS-CLUSTER-REGION
SERVICE_ACCOUNT_NAMESPACE=fargate-container-insights
SERVICE_ACCOUNT_NAME=adot-collector
SERVICE_ACCOUNT_IAM_ROLE=EKS-Fargate-ADOT-ServiceAccount-Role
SERVICE_ACCOUNT_IAM_POLICY=arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

eksctl utils associate-iam-oidc-provider \
--cluster=$CLUSTER_NAME \
--approve

eksctl create iamserviceaccount \
--cluster=$CLUSTER_NAME \
--region=$REGION \
--name=$SERVICE_ACCOUNT_NAME \
--namespace=$SERVICE_ACCOUNT_NAMESPACE \
--role-name=$SERVICE_ACCOUNT_IAM_ROLE \
--attach-policy-arn=$SERVICE_ACCOUNT_IAM_POLICY \
--approve
```

※名前空間fargate-container-insights用のFargate Profileを作成しておく

### マニュフェストをダウンロード
```
wget https://raw.githubusercontent.com/aws-observability/aws-otel-collector/main/deployment-template/eks/otel-fargate-container-insights.yaml
sed -i -e 's/YOUR-EKS-CLUSTER-NAME"/<クラスター名>"/g' otel-fargate-container-insights.yaml
sed -i -e 's/region: us-east-1/region: <リージョンコード>/g' otel-fargate-container-insights.yaml
```

### マニュフェストファイルデプロイ
```
kubectl apply -f otel-fargate-container-insights.yaml
```

