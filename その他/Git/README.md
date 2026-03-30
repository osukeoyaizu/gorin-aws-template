## 公開Webサーバーに.gitディレクトリが残っている場合にソースコードを確認する
### .gitディレクトリを丸ごとダウンロード
wget -r http://xxxx/.git

### 各コミットの差分(patch)を表示
git log -p
