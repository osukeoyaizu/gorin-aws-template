## task1
「OpenSearchのダッシュボード」→「Security」→「Internal users」からSecretsManagerの情報のユーザーを作成する

## task2
「OpenSearchのダッシュボード」→「Security」→「Roles」→「Create role」

### ロール作成
Name:limited_access_role

Cluster Permissions:indices:data/read/msearch

Index:employee

Index permissions:read

Exclude:salary

Anonymization:email

## task3
「task2で作成したロール選択」→「Mapped usersタブ」→task1で作成したユーザーをMapする

## task4
task1で作成したユーザーでログインする

「OpenSearchのダッシュボード」→「Dev Tools」で課題文のクエリを実行する

emailの値を回答する
