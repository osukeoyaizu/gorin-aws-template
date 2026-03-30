## DynamoDB
### 環境変数を設定
```
export SERVICE=dynamodb
export RELEASE_VERSION=$(curl -sL https://api.github.com/repos/aws-controllers-k8s/${SERVICE}-controller/releases/latest | jq -r '.tag_name | ltrimstr("v")')
export ACK_SYSTEM_NAMESPACE=ack-system
export AWS_REGION={リージョン}
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
export CLUSTER_NAME={クラスター名}
 ```

## ECR Public へログイン
```
aws ecr-public get-login-password --region us-east-1 | \
    helm registry login --username AWS --password-stdin public.ecr.aws
```

## コントローラーのインストール
```
helm install --create-namespace -n $ACK_SYSTEM_NAMESPACE \
    ack-$SERVICE-controller \
    oci://public.ecr.aws/aws-controllers-k8s/$SERVICE-chart \
    --version=$RELEASE_VERSION \
    --set=aws.region=$AWS_REGION
```



## EKS Pod Identity の信頼ポリシーを使用して IAM ロールを作成
```
aws iam create-role \
    --role-name ack-${SERVICE}-controller \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {
          "Service": "pods.eks.amazonaws.com"
        },
        "Action": [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }]
    }'
```

## DynamoDB ポリシーをアタッチ
```
aws iam attach-role-policy \
    --role-name ack-${SERVICE}-controller \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

## Pod Identity Association を作成
```
aws eks create-pod-identity-association \
    --cluster-name $CLUSTER_NAME \
    --namespace $ACK_SYSTEM_NAMESPACE \
    --service-account ack-${SERVICE}-controller \
    --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/ack-${SERVICE}-controller
```

## 反映するためにコントローラーを再起動
```
kubectl rollout restart deployment -n $ACK_SYSTEM_NAMESPACE \
    ack-${SERVICE}-controller-dynamodb-chart
```
