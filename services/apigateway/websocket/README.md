## websocatコマンドインストール
```
sudo wget -qO /usr/local/bin/websocat https://github.com/vi/websocat/releases/latest/download/websocat.x86_64-unknown-linux-musl
```
```
sudo chmod a+x /usr/local/bin/websocat
```

## 接続コマンド
```
websocat wss://{APIドメイン}/{ステージ}
```
