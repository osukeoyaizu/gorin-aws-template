## task1
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

## task2
インスタンスのロールにAmazonSSMManagedInstanceCoreの権限をアタッチする

## task3

### ルート変更
route DELETE 169.254.169.254

route -p ADD 169.254.169.254 MASK 255.255.255.255 {Subnet default Gateway IP}

{Subnet default Gateway IP}・・・route printコマンドを実行して、最初のネットワーク宛先 0.0.0.0 のゲートウェイIP

### プロキシ設定変更
netsh winhttp show proxy
netsh winhttp reset proxy

### ファイアウォールルール変更
wf

→アウトバウンドルールで「Block443Out」を削除する
    
### 時刻同期
W32tm /resync /force
    
### サービス再起動
Restart-Service AmazonSSMAgent

