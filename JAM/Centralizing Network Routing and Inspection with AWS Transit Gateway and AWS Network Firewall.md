## task1
VPC-Aのアタッチメントを作成

VPCルートテーブル(spoke-vpc-a-workload-subnet-route-table)に宛先:0.0.0.0/0,ターゲット:トランジットゲートウェイ

トランジットゲートウェイルートテーブル(tgw-spoke-route-table)にVPC-Aのアタッチメントを関連付ける

トランジットゲートウェイルートテーブル(tgw-firewall-route-table)にVPC-A宛てのトラフィックをVPC-Aのアタッチメントに送信するルートを作成する。

## task2
Network Firewallのルールグループ(ICMP-Stateless-Rule-Group)でドロップをパスに変更する

## task3
Network Firewallのルールグループ(Domain-Deny-List-Stateful-Rule-Group)の送信元IPを10.0.0.0/8に変更する


### ファイアウォールポリシーにマネージドステートフルルールグループを追加する
Domain and IP rule groupsをすべて選択して追加する

ステートフルルールグループに2つのThreat signature rule groupsを追加する(ThreatSignaturesEmergingEventsActionOrder,ThreatSignaturesExploitsActionOrder)

## task4
Network Firewallのルールグループ(HTTP-Ingress-Stateful-Rule-Group)でドロップをパスに変更する
