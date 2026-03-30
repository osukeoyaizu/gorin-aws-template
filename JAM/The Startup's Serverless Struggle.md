## task1
APIGatewayのLambda関数をCorrectImageProcessorに変更する

APIGatewayをデプロイする

CorrectImageProcessor関数のタイムアウト時間を1分にする

## task2
### 解き方①
processed-jam.jpgというファイルをoutput用s3バケットにアップロードする

### 解き方②
input用のs3バケットでCorrectImageProcessor関数のイベント通知を作成する

Lambda関数のIAMロールポリシーを変更してS3へのアクセスを許可する
