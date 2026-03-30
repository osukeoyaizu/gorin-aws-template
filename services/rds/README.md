## csvファイルインポート
### MySQL
```
LOAD DATA LOCAL INFILE '<ファイルパス>'
INTO TABLE <テーブル名>
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```
### PostgreSQL
```
cat <ファイルパス> |  psql -U <ユーザー名> -W -h <ホスト名> -d gorin -c "\copy devices FROM STDIN WITH (FORMAT csv, HEADER true)"
```

## RDSを暗号化
1.スナップショットを取得

2.暗号化チェックを入れてスナップショットをコピー

3.コピーしたスナップショットからデータベース復元

## gravitonインスタンス
c6g.medium や t4g.medium など g がついたインスタンス

## フェイルオーバー
リーダーインスタンスのアクションからフェイルオーバーを選択する

## SQL ServerをS3バケットからリストア
### オプショングループを作成
エンジン:sqlserver-se

#### オプションの追加
オプション名:SQLSERVER_BACKUP_RESTORE

IAM:新しいロールの作成

**RDSインスタンスの変更からオプショングループを変更**

### WindowsのSSMSに接続し、リストアコマンドを実行する
```
exec msdb.dbo.rds_restore_database 
@restore_db_name='{データベース名}', 
@s3_arn_to_restore_from='arn:aws:s3:::XXX/XXX.bak';
```

## 監査ログ
### MySQLで変更系のクエリを出力
#### オプショングループ作成
エンジン:mysql

#### オプションの追加
オプション名:MARIADB_AUDIT_PLUGIN

オプション設定の「SERVER_AUDIT_EVENTS*」の値を「QUERY_DML」

すぐに適用:Yes

#### RDSを変更
ログのエクスポート:監査ログ

オプショングループ:作成したもの

すぐに適用


## IAM認証

### 接続側に必要なIAMポリシー
```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rds-db:connect"
            ],
            "Resource": [
                "arn:aws:rds-db:{region}:{account_id}:dbuser:{リソースID}/{ユーザー}"
            ]
        }
    ]
}
```

### 設定
データベース認証オプション:「パスワードと IAM データベース認証」

### MySQL
#### ユーザー作成
```sql
CREATE USER {ユーザー}  IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';
```

#### 権限付与
```sql
GRANT ALL PRIVILEGES ON {データベース}.{テーブル} TO '{ユーザー} '@'%';
```

#### 権限確認
```sql
SHOW GRANTS FOR '{ユーザー}'@'%';
```

### PostgreSQL
#### ユーザー作成
```sql
CREATE USER {ユーザー} WITH LOGIN;
```

#### 権限付与
```sql
GRANT rds_iam to {ユーザー};
```

#### 権限確認
```sql
GRANT ALL ON public.users TO {ユーザー};
```


