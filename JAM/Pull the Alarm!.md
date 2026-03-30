## task1
### アラーム作成
メトリクス:EC2インスタンスのCPUUtilization

期間:1分

70以上

SNSトピック:OperationsTeam

アラーム名:high-cpu-utilization

## task2
### アラーム作成
メトリクス:CWAgentのdisk_used_percent

期間:1分

85以上

SNSトピック:OperationsTeam

アラーム名:low-ebs-capacity

## task3
### ダッシュボード作成
ダッシュボード名:PartyParrotMonitor

### ウィジェット追加

#### ウィジェット①
メトリクス:EC2インスタンスのCPUUtilization

ウィジェット名:CPU Utilization

#### ウィジェット③
メトリクス:CWAgentのdisk_used_percent

ウィジェット名:EBS Capacity

#### ウィジェット③
アラームのステータス:task1,task2のアラーム

ウィジェット名:Alarm Status
