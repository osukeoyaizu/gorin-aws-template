## task1

### VPCルートテーブル(Spoke-1-VPC-Route-Table)のルート追加
送信先:0.0.0.0

ターゲット:Transit Gateway

### VPCルートテーブル(tgw-attach-rtb-a)のルート追加
送信先:0.0.0.0

ターゲット:ゲートウェイロードバランサー(Output PropertiesのGatewayLoadBalancerEndpointIdAZa)

### VPCルートテーブル(natgw-rtb-a)のルート追加
送信先:10.0.0.0/24

ターゲット:ゲートウェイロードバランサー(Output PropertiesのGatewayLoadBalancerEndpointIdAZa)


## task2
### VPCルートテーブル(appliance-rtb-a)のルート追加
送信先:10.0.1.0/24

ターゲット:Transit Gateway

### トランジットゲートウェイルートテーブル(Transit Route Table)の伝播作成

伝播するアタッチメント:Spoke2-VPC-Attachment

## task3
### トランジットゲートウェイアタッチメントのコンプライアンスモードを有効化する
VPC アタッチメントを選択し、アクション、トランジットゲートウェイ アタッチメントの変更、コンプライアンスモード

3つのアタッチメントで有効化する
