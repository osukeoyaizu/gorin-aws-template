## task1
### Canvasデータセットを作成し、合計セル数を求める
「SageMaker Canvas」→「jam-ba-userでCanvasを開く」→「データセット」→「Import data」→「Tabular」

データソース:s3

バケット名:games-aiml-jam-sagemaker-data-{account-id}-{region}

ファイル名:gamestelemetrydata.csv

**※Dataset detailsから合計セル数を求める**
```
28602
```


## task2
```
apm, uniqueunitsmade
```


## task3
「My Models」→「New model」→「任意のモデル名を入力」→「Create」→「task1で作成したデータセット」

Select a column to predict:leagueindex

apmとuniqueunitsmadeのチェックを外す

**※Quick buildをクリックしてAccuracyの値(66.262)を回答する**


## task4
### モデルをデプロイする
Selected model version:jam

Deployment name:任意の名前

Instance type:ml.m5.large

Instance count:1

**Deployment nameを回答する**
