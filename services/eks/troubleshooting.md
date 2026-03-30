## ノードグループを作成したのにノードが作成されない
- アクセスエントリを確認
- セキュリティグループを確認(お互いに通信できる必要がある)
- EC2にSSMで接続し、以下のコマンドを実行
```
journalctl -u kubelet
```
### 修正手順
- https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/hybrid-nodes-troubleshooting.html
