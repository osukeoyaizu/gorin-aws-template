## podのログ確認
```
kube-system logs {ポッド名} -n {名前空間}
```

## リソースをyaml形式で取得する
```
kubectl get {リソースタイプ} {リソース名} -n {名前空間} -o yaml > {保存先ファイル名}.yaml
```

## リソースを再起動
```
kubectl rollout restart {リソースタイプ} {リソース名} -n {名前空間}
```


## コンテナに入る
```
kubectl exec -it -n {名前空間} {Pod名} -- /bin/bash
```