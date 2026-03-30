## task1
エージェントのモデルを「Nova Lite」にして保存して終了

## task2
### ナレッジベース作成
ベクトルストアを含むナレッジベース

名前:sports-knowledge-base

ロール:AmazonBedrockExecutionRoleForKnowledgeBase

s3のURI:「sports-products-{region}-{account-id}」の arn

埋め込みモデル:Titan Text Embeddings v2

#### ベクトルデータベース

ベクトルストアの作成方法:既存のベクトルストアを使用

ベクトルストア:OpenSearch Serverless

コレクションarn:OpenSearch Serverlessで作成済のコレクションARN

ベクトルインデックス名:bedrock-knowledge-base-index

ベクトルフィールド名:「OpenSearch」→「Serverless:Collections」→「インデックス(bedrock-knowledge-base-index)」→ベクトルフィールド名の値

テキストフィールド名:text

Bedrock マネージドメタデータフィールド名:metadata


## task3
エージェントの編集し、task2で作成したナレッジベースを指定する

エージェント向けナレッジベースの指示で以下の値を入力
```
This knowledge base contains product catalog information including Product Id, Name, Type, Color, Weight, Size, Company, and Price for each item.
```

## task4
```
The restock order for 50 units of Product ID SP001 has been successfully created.
```
