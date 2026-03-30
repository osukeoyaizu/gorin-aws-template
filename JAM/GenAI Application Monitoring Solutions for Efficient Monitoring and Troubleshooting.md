## task1
モデルアクセスを有効化する

出力プロパティのApplicationDomainに接続し、Invoke Modelをクリックする

### CloudWatchアラーム作成
メトリクス:amazon.nova-lite-v1:0のInvocationLatency

期間:1分

3000以上

名前:任意

## task2
### CloudWatchアラーム作成
メトリクス:amazon.nova-lite-v1:0のInputTokenCount

期間:15分

2500以上

名前:任意

## task3
「CloudWatch」→「Application Signals」→「RUM」
### アプリケーションモニターを追加する
モニター名:任意

Application domain list:出力プロパティのApplicationDomain

カスタムイベントにチェックをつける

既存のIDプールを選択する

サンプルコード(HTML)のscriptタグを除いたコードをコピーし、cwrum.jsファイルを作成し、s3バケットにアップロードする

アプリケーションのページを更新し、Invoke Modelをクリックする
