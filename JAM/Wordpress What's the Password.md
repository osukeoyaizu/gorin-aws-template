## task1
WordPressの管理画面から「All-in One WP Migration」プラグインをインストールし、アクティブ化する。

出力プロパティのWordPressBackupFileのURLからダウンロードしたファイルをインポートする。


## task2
```
sudo curl https://aws-jam-challenge-resources-{region}.s3.amazonaws.com/wp-migration-blunders/reset.php.txt -o /opt/bitnami/wordpress/reset.php
```
```
sudo chmod 775 /opt/bitnami/wordpress/reset.php && sudo chown bitnami:daemon /opt/bitnami/wordpress/reset.php
```

ブラウザからアクセスする(public-ipは出力プロパティのWordpressAdminPanelから確認する)
```
http://{public-ip}/reset.php?pass=51yH!29xgT
```

変更したパスワードで再度ログインする

ユーザー名:user

パスワード:51yH!29xgT

