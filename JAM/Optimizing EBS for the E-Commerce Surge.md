## task1
### EBSのボリュームタグを追加する(ボリューム変更前に設定する)
Key: Name | Value: Production-Volume

Key: challenge | Value: extend-windows-disk

### EBSのボリュームを変更する
Volume type | General Purpose SSD (gp3)

Volume Size (GiB) | 100

Volume IOPS | 5000

Througput (MiB/s) | 150

## task2
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

## task3(何もしなくてもクリアになる)
```
Windows Search を使用するか、「ファイル名を指定して実行」ダイアログ（Win + R）で「」と入力しdiskmgmt.msc、Enter キーを押します。ディスク管理ユーティリティが開きます。
[ディスクの管理]メニューで、[操作]、[ディスクの再スキャン]を選択します。
ディスク 0の横にある拡張ドライブのコンテキスト (右クリック) メニューを開き、ボリュームの拡張を選択します。
ボリュームの拡張ウィザードで、「次へ」を選択します。使用可能な最大容量を選択したまま、「次へ」をクリックしてウィザードを完了します。
ディスクを拡張した後、新しいディスク サイズが であるかどうかを確認してください100 GB。
詳細については、次の AWS ドキュメントを参照してください。

> https://docs.aws.amazon.com/ebs/latest/userguide/recognize-expanded-volume-linux.html
```
