## Studio Notebook
### リアルタイムストリームデータを処理し、Redis（ElastiCache）に集計結果を保存
#### テーブル作成
```
%flink.ssql
CREATE TABLE `player_data` (
    `player_id` STRING,
    `speed` BIGINT,
    `distance` BIGINT,
    `event_time` TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
)
WITH (
    'connector' = 'kinesis',
    'stream' = '[Enter stream name here]',
    'aws.region' = '[Enter AWS region name here]',
    'scan.stream.initpos' = 'TRIM_HORIZON',
    'format' = 'json'
);
```

#### プレイヤー数をリアルタイムで確認
```
%flink.ssql(type=update)
select count(distinct player_id) from player_da
```

#### Redisに集計結果を保存
```
CREATE TABLE `total_distance` (
  `zset_key` STRING,
  `total_distance` BIGINT,
  `player_id` STRING
)
WITH (
 'connector' = 'redis',
 'redis-mode' = 'cluster',
 'command' = 'zincrby',
 'cluster-nodes' = '[elasticache-redis-host:port]'
);
```
command = 'zincrby' → RedisのZINCRBYコマンドを使ってスコア付きソートセット（ZSET）に距離を加算

zset_key は固定で 'leaderboard:total_distance' → リーダーボードのキー

#### 集計クエリ
```
INSERT INTO total_distance
SELECT 'leaderboard:total_distance' as zset_key, SUM(distance), player_id
FROM TABLE(
        TUMBLE(TABLE `player_data`, DESCRIPTOR(event_time), INTERVAL '30' SECOND))
GROUP BY window_start, window_end, player_id
```
TUMBLE → 30秒ごとの時間窓で集計
