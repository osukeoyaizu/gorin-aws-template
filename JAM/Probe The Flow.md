## task1
VPCフローログをS3とCloudWatchに保存する

## task2
### CloudWatchのロググループでメトリクスフィルターを作成する

フィルターパターン:REJECT

メトリクス名前空間: vpcflowlogs

メトリクス名: NetworkRejects

### アラーム作成
メトリクス:task1のメトリクス

1より大きい

アラーム名: NetworkRejects


## task3
Athenaでテーブル作成
YYYY,MM,ddをs3に存在する値に変更する
```
CREATE EXTERNAL TABLE IF NOT EXISTS `vpc_flow_logs` ( version int, account_id string, interface_id string, srcaddr string, dstaddr string, srcport int, dstport int, protocol bigint, packets bigint, bytes bigint, start bigint, `end` bigint, action string, log_status string, vpc_id string, subnet_id string, instance_id string, tcp_flags int, type string, pkt_srcaddr string, pkt_dstaddr string, region string, az_id string, sublocation_type string, sublocation_id string, pkt_src_aws_service string, pkt_dst_aws_service string, flow_direction string, traffic_path int ) PARTITIONED BY (`date` date) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' ' LOCATION 's3://DOC-EXAMPLE-BUCKET/AWSLogs/{account_id}/vpcflowlogs/{region_code}/' TBLPROPERTIES ("skip.header.line.count"="1");
```
```
ALTER TABLE vpc_flow_logs ADD PARTITION (`date`='YYYY-MM-dd') LOCATION 's3://DOC-EXAMPLE-BUCKET/AWSLogs/{account_id}/vpcflowlogs/{region_code}/YYYY/MM/dd';
```
```
SELECT * FROM vpc_flow_logs WHERE date = DATE('YYYY-MM-DD') LIMIT 100;
```
