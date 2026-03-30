## 事前準備

### VPCルートテーブルのルート追加

#### AWS-Side-Private

送信先:オンプレサイドのIPv6 CIDR

ターゲット:トランジットゲートウェイ

#### Onprem-Side-Private

送信先:AWSサイドのIPv6 CIDR

ターゲット:トランジットゲートウェイ

### セキュリティグループでインバウンドルール追加

#### AWS-Side-Endpoint
タイプ:DNS(UDP,TCP)

ソース:オンプレサイドのIPv6 CIDR

#### Onprem-Side-Endpoint
タイプ:DNS(UDP,TCP)

ソース:AWS再度のIPv6 CIDR

### Route53 リゾルバーのルール編集

#### ipv4-onprem-internal
Onprem-Side-InboundのどちらかのIPv4アドレスをターゲットIPアドレスとして登録

#### ipv6-onprem-internal
Onprem-Side-InboundのどちらかのIPv6アドレスをターゲットIPアドレスとして登録

## task1
インスタンス(Onprem-Test-IPv4-Only)に接続
```
dig +short task-a.aws.internal TXT @<AWS-Side-Inbound IPv4 HERE>
```

## task2
インスタンス(Onprem-Test-IPv4-Only)に接続
```
dig +short task-a.aws.internal TXT @<AWS-Side-Inbound IPv6 HERE>
```

## task3
インスタンス(AWS-Test-IPv4-Only)に接続
```
dig +short task-c.ipv4.onprem.internal TXT
```

## task4
インスタンス(AWS-Test-IPv4-Only)に接続
```
dig +short task-d.ipv6.onprem.internal TXT
```
