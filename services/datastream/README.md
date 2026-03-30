## EFO(拡張ファンアウト)
### aws cliでEFO作成
```
aws kinesis register-stream-consumer \
--stream-arn {データストリームのARN} \
--consumer-name {コンシューマー名}
```

### Lambdaでトリガー作成
- Kinesisを選択
    - Consumerで作成したものを選択する

#### AWS CLIで設定する場合
- --starting-position : Lambda が Kinesis のどこから読み始めるかを指定する
- --maximum-batching-window-in-seconds : Lambda に渡す前にデータを最大何秒までためるか
- --batch-size : Lambda に渡す 1 回のバッチの最大レコード数
```
aws lambda create-event-source-mapping \
--function-name {LambdaのARN} \
--batch-size 100 \
-maximum-batching-window-in-seconds 5 \
--starting-position LATEST
```
