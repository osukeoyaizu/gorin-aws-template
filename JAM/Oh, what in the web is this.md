## task1
### InternalBlogWordpressURLにアクセスしてコマンド実行
```
sudo chmod 775 /opt/bitnami/wordpress/wp-includes
sudo /opt/bitnami/ctlscript.sh restart apache
```


## task2
### ポート確認コマンド
```
sudo netstat -tulnp | grep LISTEN
```

### InternalBlogSSHAccessURLにアクセスしてコマンド実行
```
sudo chmod 775 /opt/bitnami/wordpress
sudo /opt/bitnami/ctlscript.sh restart apache
sudo sed -i 's/127.0.0.1:3306/127.0.0.1:64331/g' /opt/bitnami/wordpress/wp-config.php
sudo /opt/bitnami/ctlscript.sh restart
```
