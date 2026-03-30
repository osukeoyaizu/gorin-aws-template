## task1
```
{datastream名},{redisホスト名:6379}
```

## task2
Studio Notebookで実行
### テーブル作成
「stream」と「aws.region」の値を設定して実行する
```
%flink.ssql
CREATE TABLE `player_data` (
    `player_id` STRING,
    `speed` BIGINT,
    `distance` BIGINT,
    `event_time` TIMESTAMP(3),
     WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND -- watermark for late arrival handling
)
WITH (
    'connector' = 'kinesis', -- connect to the kinesis stream
    'stream' = '[Enter stream name here]', -- example: my-kinesis-stream
    'aws.region' = '[Enter AWS region name here]', -- example: eu-west-1
    'scan.stream.initpos' = 'TRIM_HORIZON', -- read from the very beginning of the stream
    'format' = 'json' -- source data in json format
);
```

### ユーザー数確認クエリ
```
%flink.ssql(type=update)
select count(distinct player_id) from player_data
```

## task3
### テーブル作成
「cluster-nodes」の値を設定して実行する
```
%flink.ssql
CREATE TABLE `total_distance` (
  `zset_key` STRING, -- Key of ZSET must be hardcoded to 'leaderboard:total_distance'
  `total_distance` BIGINT, -- Value
  `player_id` STRING -- Key
)
WITH (
 'connector' = 'redis', -- connect to redis database, Elasticache
 'redis-mode' = 'cluster', -- connect using cluster mode
 'command' = 'zincrby', -- Use redis operation ZINCRBY for all queries
 'cluster-nodes' = '[elasticache-redis-host:port]' -- example: my-elasticache-redis-host:6379
);
```

### クエリ実行
```
%flink.ssql(type=update)
INSERT INTO total_distance SELECT 'leaderboard:total_distance' as zset_key, SUM(distance), player_id
FROM TABLE(
        TUMBLE(TABLE `player_data`, DESCRIPTOR(event_time), INTERVAL '30' SECOND))
GROUP BY window_start, window_end, player_id
```
