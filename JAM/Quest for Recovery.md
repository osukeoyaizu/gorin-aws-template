## task1
### wordpressのバージョン取得
```
sudo cat /opt/bitnami/wordpress/wp-includes/version.php | grep -i '\$wp_version' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'
```
### バージョンのインストール用ファイルをダウンロード(x.x.xを最初のコマンドで出力された値に変更して実行する)
```
version='x.x.x';sudo curl https://wordpress.org/wordpress-$version.tar.gz -o /tmp/wordpress-$version.tar.gz;
```

### ファイルを置き換える
```
tar -xvf /tmp/wordpress-$version.tar.gz -C /tmp
cp /tmp/wordpress/index.php /opt/bitnami/wordpress/index.php
cp /tmp/wordpress/wp-settings.php /opt/bitnami/wordpress/wp-settings.php
cp /tmp/wordpress/wp-includes/theme.php /opt/bitnami/wordpress/wp-includes/theme.php
cp /tmp/wordpress/wp-includes/js/jquery/jquery.min.js /opt/bitnami/wordpress/wp-includes/js/jquery/jquery.min.js
rm -f /opt/bitnami/wordpress/wp-includes/n34r.php
rm -f /opt/bitnami/wordpress/wp-includes/n64r.php
sudo /opt/bitnami/ctlscript.sh restart
```

## task2
```
sudo wp user list
```
```
sudo wp user delete armitage --yes
```

## task3
```
sudo journalctl -u ssh
```
### 回答
```
wproot
```
