## task1
### ナレッジベース作成
指示通りに作成(ベクトルストアは作成されているOpenSearch Serverless Collection)


## task2
### Lambda(find-secretkey-lambda)の環境変数設定
キー:KNOWLEDGE_BASE_ID
値:task1で作成したナレッジベースID

### Lexのインテントから構築してテストする

### 回答
```
FinanceBOT
```

## task3
### s3に課題文からダウンロードしたファイルをアップロードする

s3://application-data-bucket-{account-id}/hr.txt.metadata.json
s3://application-data-bucket-{account-id}/Finance/finance.txt.metadata.json

### ナレッジベースを同期する

## task4
### Lambda(metadata-filter-lambda)の環境変数設定
キー:KNOWLEDGE_BASE_ID
値:task1で作成したナレッジベースID

### LexのLambda関数を変更
「Lex」 → 「ボット」 → 「エイリアス」 → 「言語」

metadata-filter-lambdaを選択する

### 回答
```
HRBOT
```
