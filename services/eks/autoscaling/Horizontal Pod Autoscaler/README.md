## Horizontal Pod Autoscaler を使用してポッドデプロイをスケールする

### メトリクスサーバーでのリソース使用状況の表示
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/metrics-server.html

**メトリクスサーバーをデプロイ(fargateの場合はcomponents.yamlのポート10250を10251に置き換える)**
```
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
**デプロイする**
```
kubectl apply -f components.yaml
```

**Podsが実行されているか確認**
```
kubectl get deployment metrics-server -n kube-system
```

**メトリクスサーバーが動作しているかテストする**
```
kubectl top nodes
```

### Horizontal Pod Autoscaler を使用してポッドデプロイをスケールする
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/horizontal-pod-autoscaler.html

**アプリケーションをデプロイ**
```
kubectl apply -f <マニュフェストファイル>
```

**デプロイ用の Horizontal Pod Autoscaler リソースを作成**
```
kubectl autoscale deployment <deployment名> --cpu-percent=50 --min=2 --max=4 -n <名前空間名>
```

**デプロイのスケールアウトを監視する**
```
kubectl get hpa <deployment名> -n <名前空間名>
```

**詳細を確認する**
```
kubectl describe hpa <deployment名> -n <名前空間名>
```

**※autoscaler削除方法**
```
kubectl delete horizontalpodautoscaler.autoscaling/<deployment名> -n <名前空間名>
```


**※デプロイメントにresourceを追加しないとメトリクスを収集できない**

```
    spec:
      containers:
      - image: nginx  #コンテナイメージを指定する
        imagePullPolicy: Always
        name: lab2-app
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "1"
          requests:
            cpu: "0.5"
```

## スケールアウトの確認
**podに入る**
```
kubectl exec -it <Pod名> -n <名前空間名> -- /bin/bash
```
**コマンドインストール**
```
apt-get update
apt-get install -y stress dstat
```

**負荷をかける**
```
stress -c 2
```

**Pod内で確認**
```
dstat -c
```

**確認**
```
kubectl get hpa -w <deployment名> -n <名前空間名>
```
