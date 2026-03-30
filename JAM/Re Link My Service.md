## task1
### NACL(Consumer Private Subnet ACL)のインバウンドルール追加
ルール:9​

タイプ:HTTP (80)

ソース:10.0.0.0/16

許可/拒否アクション:「許可」

### NACL(Consumer Private Subnet ACL)のアウトバウンドルール追加
ルール:9​

タイプ:カスタムTCP

ポート範囲:1024-65535

送信先:10.0.0.0/16

許可/拒否アクション:「許可」


### セキュリティグループ(Consumer Endpoint Interface SG)のインバウンドルール追加
タイプ:HTTP

ソース:10.0.0.0/16

## task2

### Unhealthyのインスタンス(TargetInstance3)のセキュリティグループのインバウンドルール編集
タイプ:カスタムTCP

ポート範囲:8080

ソース:20.0.0.0/16

### クロスゾーン負荷分散を有効にする
NLB → 属性 → クロスゾーン負荷分散を有効にする
