## ソースエンドポイント
### MySQL
パラメータグループのbinlog_formatの値をROWにする

同期させてからタスク開始

### PostgreSQL
パラメータグループのlogical_replicationの値を1にする

同期させてからタスク開始


## ターゲットエンドポイント
追加の接続属性(カラム名を含めたcsvファイルを出力)
```
addColumnName=True;compressionType=NONE;csvDelimiter=,;csvRowDelimiter=\n;datePartitionEnabled=false;
```
※ロールにS3FullAccessとKMSの権限をアタッチする


## Oracleソース
### CDC
- 以下のSQLをOracleで実行
```
BEGIN
    rdsadmin.rdsadmin_util.alter_supplemental_logging(
    p_action => 'ADD'
    );
END;


BEGIN
    rdsadmin.rdsadmin_util.alter_supplemental_logging(
    p_action   => 'ADD',
    p_type     => 'PRIMARY KEY'
    );
END;
```
- YESになっているかを確実
```
SELECT supplemental_log_data_min,
        supplemental_log_data_pk
FROM v$database;
```
