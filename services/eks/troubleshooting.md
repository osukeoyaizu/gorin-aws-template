## ノードグループを作成したのにノードが作成されない
- アクセスエントリを確認
- セキュリティグループを確認(お互いに通信できる必要がある)
- EC2にSSMで接続し、以下のコマンドを実行
```
journalctl -u kubelet
```
### 修正手順
- https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/hybrid-nodes-troubleshooting.html


## AccessDenied: Not authorized to perform sts.AssumeRoleWithWebIdentity
- サービスアカウントに紐づくIAMロールの信頼ポリシーがおかしい

## Cluster Autoscalerがうまく動かない
https://repost.aws/ja/knowledge-center/amazon-eks-troubleshoot-autoscaler
- AGにタグ付けが必要


## ingressが消せない
```
 kubectl patch ingress <ingress名> -n <名前空間>   -p '{"metadata": {"finalizers": []}}' --type=merge
```