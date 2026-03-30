## task1
作成済みのWAFをALBに関連付ける

## task2
### AWSマネージドルール追加
「Core rule set」を追加する

### 独自のルールを作成
ルール名:RateBasedRule

タイプ:レートベースのルール

レート制限:100

評価ウィンドウ:5分

検査範囲と速度制限:ルールステートメントの基準に一致するリクエストのみを考慮する

Inspect:URI Path

Match type:Ends with string

String to match:login

アクション:ブロック

## task3
### IP sets 作成
名前:SecurityAllowedIPs
IP address:課題の指示に従う

### 独自のルールを作成
ルール名:SecurityAllowedIPsRule

Inspect:Originates from an IP address in

IP set:SecurityAllowedIPs

IP address to use as the originating address:IP address in header

Header field name:X-Client-Ip

Action:Allow

Custom request:Key=Authorization,Value=QWxsb3dlZElwcw==

優先度を一番高くする
