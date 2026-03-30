## task1
### プライベートホストゾーン作成
ドメイン名:example.test

### レコード追加
レコード名:catとdogの2つ

トラフィックのルーティング先:ALBへのエイリアス

### ALBルール
#### default
レスポンスコード:404

レスポンス本文:Not Found

#### cat
ホストヘッダー条件値:cat.example.test

ターゲットグループ:traget-cat

#### dog
catと同じように


