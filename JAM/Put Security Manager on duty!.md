## task1
### ソースエンドポイント作成
エンドポイント識別子:任意

ソースエンジン:SAP Sybase ASE

シークレット:jam/dms-user-sap-ase-credential

IAMロール:出力プロパティのDMSIAMRole

SSLモード:すべてを確認

CA証明書:課題文からダウンロードしたファイル

データベース名:pubs2

## task2
### StepFunctions(jam-create-db-rds-sql-server)実行
ロールにlambda:InvokeFunctionを追加し、以下のJSONで実行する
```
{ 
    "RDSSecretManagerARN": "<出力プロパティのRDSSecretManagerARN>",
    "DB_NAME": "pubs2"
}
```

### ターゲットエンドポイント作成
RDS DBインスタンスの選択にチェックをつける

シークレット:jam/dms-user-rds-sql-server

IAMロール:出力プロパティのDMSIAMRole

データベース名:pubs2

## task3
### タスク作成
名前:任意

タスクタイプ:移行のみ

ターゲットテーブル準備モード:切り詰める

### テーブルマッピングの選択ルールで新しいルールを追加
スキーマ名:dbo

スキーマテーブル名:%

移行前評価をオンにするのチェックを外す
