## task1
### CanvasのTabularを使用
**SageMaker-AI → Canvas → Data Wrangler → Import and prepare → Tabular**

### s3からデータインポート
**Select a data source → S3 → my-challenge-bucket-101-<account-id>-<region>/data/basketball_games.csv → import**

### 欠損値補完
**Add transform → Handle missing → input columns → Select all**

### 重複削除
**Add transform → Manage rows → Transform → Drop duplicates**

### s3にエクスポートする
**Export → Export data to Amazon S3 → s3://my-challenge-bucket-101-768236330706-us-west-2/clean/ → Export**

## task2
**キャンバスのページを更新して出力されたファイルパスを取得する**

**train.pyの#TODO部分を指示通りの値に変更する**

**実行して出力のjob名を回答する**

## task3
**deploy.pyの#TODO部分を指示通りの値に変更する**

**実行して出力のエンドポイント名を回答する**

## task4
**predict.pyを実行してConfidenceの数値を出力する(○○.○)**

