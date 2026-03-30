## task1
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

## task2
### ルート変更
route DELETE 169.254.169.254

route -p ADD 169.254.169.254 MASK 255.255.255.255 {Subnet default Gateway IP}

{Subnet default Gateway IP}・・・route printコマンドを実行して、最初のネットワーク宛先 0.0.0.0 のゲートウェイIP
    
### サービス再起動
Restart-Service AmazonSSMAgent


**進捗確認を10回程度クリックするとクリアになる**
