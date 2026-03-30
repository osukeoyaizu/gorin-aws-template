## task1
egress

## task2
Egress用のVPCを作成する

VPCなど

アベイラビリティゾーンの数:1

パブリックサブネットの数:1

プライベートサブネットの数:1

NATゲートウェイ:1AZ内

VPCエンドポイント:なし

## task3
トランジットゲートウェイ作成

アタッチメント作成(3つ)

トランジットルートテーブル作成

トランジットルートテーブル関連付け

### トランジットルートテーブルルート編集
0.0.0.0/0, task2で作成したVPCのアタッチメント

VPC1,2へのルート作成

### VPCルートテーブル編集
VPC1,2のプライベートルートで 宛先:0.0.0.0/0,ターゲット:トランジットゲートウェイ のルート追加

task2で作成したパブリックルートでに宛先VPC1とVPC2,ターゲット:トランジットゲートウェイ の2つのルート追加

## task4
Still in the VPC console, delete the NAT Gateways

Navigate to NAT Gateways in the left-hand menu
Tick the box next to the NAT Gateway in VPC A that starts with a-nat-lab
Select Actions->Delete NAT gateway
Enter delete to confirm and select Delete
Repeat for the NAT Gateway for VPC B.
Wait until the NAT Gateways are deleted
Delete the public subnets

Navigate to Subnets in the left-hand menu
Tick the boxes next to a-public-subnet and b-public-subnet
Select Actions->Delete subnet
Ignore the warning about am:GetResourceShareAssociations permissions
Enter delete to confirm and select Delete
Delete the public route tables

Navigate to Route tables in the left-hand menu
Tick the boxes next to a-public-route-table and b-public-route-table
Select Actions->Delete route table
Enter delete to confirm and select Delete
Delete the internet gateways

Navigate to Internet gateways in the left-hand menu
Tick the box next to a-igw
Select Actions->Detach from VPC
Select Detach Internet gateway
Tick the box next to a-igw
Select Actions->Detach from VPC
Select Detach Internet gateway
Tick the boxes next to a-public-route-table and b-public-route-table
Select Actions->Delete internet gateway
Enter delete to confirm and select Delete
Select Check my progress in the Jam console when you think you are done.
