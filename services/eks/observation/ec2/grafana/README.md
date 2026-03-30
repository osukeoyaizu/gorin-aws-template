## grafana
https://techblog.ap-com.co.jp/entry/2024/04/02/115144

### 前提条件
  - kubectlとeksctlをセットアップする
  - クラスターを作成する(fargateじゃない)
  - oidcプロバイダーの作成
  - helmのインストール
  - AWS Load Balancer Controller のセットアップ

###  Prometheusのインストール
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install my-prometheus prometheus-community/kube-prometheus-stack
```

### Grafanaのインストール
```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
    --set service.type=LoadBalancer
```

### リソースをyaml形式で取得する
```
kubectl get service my-grafana  -o yaml > grafana-service.yaml
```

### grafana-service.yamlのannotationsに以下の内容を追加
```
service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
```

### マニフェスト適用
```
kubectl apply -f grafana-service.yaml
```

### パスワード、URL取得
```
kubectl get secret  my-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
export SERVICE_IP=$(kubectl get svc my-grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo http://$SERVICE_IP:80
```

### grafanaの設定
ユーザー名:admin,パスワード:上記のコマンドで取得したものを使用してログインする

サイトの内容を参考にして設定する

