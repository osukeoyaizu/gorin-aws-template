## task1
Lightsailに接続し、認証情報を取得する

ダッシュボード → 左上の「マイサイト」 → 「ネットワーク管理」 →「サイト」→「新規サイトの追加」

サイトアドレス:marketing-site

サイトタイトル:Marketing Site

管理者メールアドレス:user@example.com

## task2
コマンド実行
```
sudo chmod 775 /opt/bitnami/wordpress/wp-includes
sudo /opt/bitnami/ctlscript.sh restart apache
```
