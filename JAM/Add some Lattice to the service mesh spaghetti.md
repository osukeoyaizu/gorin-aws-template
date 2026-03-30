## task1
### Latticeのターゲットグループ作成
ターゲットタイプ:ALB

ターゲットグループ名:checkout-tg

プロトコルHTTP

プロトコルバージョン:HTTP1

VPC:checkout-vpc

### Latticeのサービス作成
サービス名:checkout-svc

カスタムドメイン名:checkout.retailstore.com

リスナープロトコル:HTTP

リスナーポート:80

ターゲットグループ:checkout-tg

## task2
###  サービスネットワーク作成
サービスネットワーク名:retailstore-servicenetwork

サービス関連付け:checkout-svc,orders-svc

VPC関連付け:ui-vpc,checkout-vpc

## task3
### Route53でレコード作成
レコード名:checkout.retailstore.com

レコードタイプ:CNAME

値:checkoutサービスのドメイン名
