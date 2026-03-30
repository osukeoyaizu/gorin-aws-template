## ログ確認コマンド
```
kubectl get secret.secretsmanager.services.k8s.aws {aws-secret.yamlのmetadata.name} -n {名前空間} -o yaml 
```
```
kubectl get events --field-selector involvedObject.name={aws-secret.yamlのmetadata.name} -n {名前空間}
```