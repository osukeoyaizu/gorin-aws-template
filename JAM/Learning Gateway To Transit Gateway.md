## task1
### Bastionインスタンスのセキュリティグループを変更する
    
ローカルPCのグローバルIPからのSSHとAll ICMP-IPv4 を許可する

### VPC1Privateインスタンスのセキュリティグループを変更する
BastionインスタンスのセキュリティグループからのSSHとAll ICMP-IPv4 を許可する

### VPC2Privateインスタンスのセキュリティグループを変更する
VPC1のCIDRからのAll ICMP-IPv4 を許可する

## task2
VPC1とVPC2のプライベートサブネットを関連付けしたVPCルートテーブルで相手のVPCのCIDR宛の通信をトランジットゲートウェイにルーティングするルートを追加する

## task3
トランジットゲートウェイルートテーブルで伝搬を作成する

ローカルPCからVPC1Privateインスタンスに接続し、VPC2PrivateインスタンスへPingする
