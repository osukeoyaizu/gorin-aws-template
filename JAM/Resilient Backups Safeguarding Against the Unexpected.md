## task1

### オートメーションタスク登録
「Systems Manager」→「メンテナンスウィンドウ」→「Backup-MaintenanceWindow」→「アクション」→「オートメーションタスクの登録」

オートメーションドキュメント:AWS-StopEC2Instance

ターゲット:Task target not required

Instanceid:課題のEC2インスタンスID

サービスロール:Production-MaintenanceWindowsExecutionRole

### メンテナンスウィンドウの次の実行時間を変更
cronで現在時刻から2分後に実行されるように設定

タイムゾーンでTokyoを指定

## task2
### オートメーションタスク登録
「Systems Manager」→「メンテナンスウィンドウ」→「Backup-MaintenanceWindow」→「アクション」→「オートメーションタスクの登録」

オートメーションドキュメント:AWS-CreateImage

ターゲット:Task target not required

Instanceid:課題のEC2インスタンスID

サービスロール:Production-MaintenanceWindowsExecutionRole

### メンテナンスウィンドウの次の実行時間を変更
cronで現在時刻から2分後に実行されるように設定

タイムゾーンでTokyoを指定

**※task1が終了すると自動的にEC2インスタンスが起動するのでインスタンスを停止させてからAMIを作成する**
