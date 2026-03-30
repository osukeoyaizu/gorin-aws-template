## パーティショニング射影
※JSONデータ
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `default`.`data` (
  `deviceId` string,
  `timestamp` string,
  `temperature` double,
  `vibration` double
)
PARTITIONED BY ( 
  `partition_date` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'FALSE',
  'dots.in.keys' = 'FALSE',
  'case.insensitive' = 'TRUE',
  'mapping' = 'TRUE'
)
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://{BUCKET_NAME}/'
TBLPROPERTIES (
  'classification' = 'json',
  'projection.enabled' = 'true',
  'projection.partition_date.type' = 'date',
  'projection.partition_date.format' = 'yyyy/MM/dd/HH',
  'projection.partition_date.range' = 'NOW-1YEARS,NOW',
  'projection.partition_date.interval' = '1',
  'projection.partition_date.interval.unit' = 'HOURS',
  'storage.location.template' = 's3://{BUCKET_NAME}/${partition_date}/'
);

```

## DynamoDBのデータをクエリ
### 前提条件
DynamoDBを作成

結果保存先のS3を作成

KMSで暗号化

### データソースの作成
データソース:DynamoDB

S3:結果保存先のS3

S3でのクエリ結果の暗号化:KMSキー

**作成後、自動でLambdaとデータカタログが作成される**

**自動作成されたLambdaのIAMロールにKMSの権限を追加する**

### QuickSightで可視化
データソースでAthenaを指定する

**QuickSightのロールにAthenaとLambdaの権限をアタッチする**



## SQL
### 現在時刻
```sql
SELECT current_timestamp;
```

### 日付フォーマット
```sql
SELECT date_format(current_timestamp, '%Y');
```

### 条件式
```sql
SELECT
  COUNT(*) AS total_requests,
  SUM(CASE WHEN status = 200 THEN 1 ELSE 0 END) AS success,
  SUM(CASE WHEN not status = 200 THEN 1 ELSE 0 END) AS miss,
  (SUM(CASE WHEN status = 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS success_rate_percentage
FROM
  app_log
WHERE
  path = '/'
```


### S3にアクセスしたユーザー数を特定するクエリ(CloudTrail証跡)
```sql
SELECT useridentity.username as user, requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
GROUP BY  useridentity.username, requestparameters
ORDER BY user;
```
