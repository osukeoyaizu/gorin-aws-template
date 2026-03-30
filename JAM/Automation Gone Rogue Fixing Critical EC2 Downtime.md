## task1
「Systems Manager」→「ステートマネージャー」

Production-StartEC2Instanceの関連付けを編集する

ドキュメント:AWS-StartEC2Instance

スケジュールあり

Rateスケジュールビルダー

毎日

## task2
Production-StopEC2Instanceの関連付けを編集する

ドキュメント:AWS-StopEC2Instance

スケジュールあり

CRON/Rate式

現在時刻から3分後の時間をCRON/RATE式で設定する

※リージョンに合わせた時間を設定する必要がある

次に指定された cron 間隔でのみ関連付けを適用するにチェックをいれる
