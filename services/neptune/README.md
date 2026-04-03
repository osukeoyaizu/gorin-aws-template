## ノートブック作成
Neptuneコンソール → ノートブック → ノートブック作成

## 頂点、エッジ登録
ノートブック → アクション → JupyterLabを開く
neptune.ipynbを実行する

## グラフ表示
ノートブック → アクション → Graph Explorerを開く

### クエリ実行
```
g.V().has('person','name','Alice')
```

```
g.V().has('person','name','Alice').outE('lives_in').inV()
```

```
g.E().hasLabel('lives_in')
```

Add Allで表示可能

## IAM認証
- cluster-xxxxxはクラスターのリソースID
```
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "neptune-db:*",
      "Resource": "arn:aws:neptune-db:{リージョン}:{アカウントID}:cluster-{xxxxx}/*"
    }
  ]
}

```