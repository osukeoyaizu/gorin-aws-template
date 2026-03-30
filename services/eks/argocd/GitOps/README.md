## 手順
### 前提条件
- hubクラスター(hub-cluster, us-east-1)
- spokeクラスター(spoke-cluster, ap-northeast-1)
- クラスターの「API サーバーエンドポイントの設定」は「パブリックおよびプライベート」
- Argo CD CLIインストール済み

### spokeクラスターのコンテキスト追加
```
aws eks update-kubeconfig --region {region} --name {spokeクラスター名}
```

### 確認
```
kubectl config get-contexts
```

### hubクラスターに切り替える
```
aws eks update-kubeconfig --region {region} --name {hubクラスター名}
```

### argocdにログインする
```
argocd login {ホスト名}　例:argocd.oyaizu.gorin.toro.toyota
```

### argocdにspokeクラスターを追加
```
argocd cluster add {spokeクラスターarn}
```

### spokeクラスターにラベル追加
```
argocd cluster set arn:aws:eks:ap-northeast-2:549209747641:cluster/spoke-cluster --label region=ap --label env=prod --grpc-web
```



### application.yamlを適用する
```
kubectl apply -f application.yaml
```






