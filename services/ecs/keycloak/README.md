
## ターゲットグループ設定
- ポート:8080
- ヘルスチェックパス:/health


## mysqlを使用する場合
Dockerfileと環境変数を変更
```
ENV KC_DB=mysql
```