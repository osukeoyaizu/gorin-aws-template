## task1
DynamoDBテーブルのストリームを新しいイメージでオンにする

Lambda関数(ddb-stream-func)をトリガーする

Lambda関数(file-upload-func)を実行する

**※クリアにならない場合は、テーブルに追加されたデータを削除し、再度実行する**

## task2
### ナレッジベース作成
ベクトルストアを含むナレッジベース

名前:ddb-knowledge-base

ロール:AmazonBedrockExecutionRoleForKnowledgeBase

s3のURI:「news3bucket」を含むバケット名の arn

埋め込みモデル:Titan Text Embeddings v2

#### ベクトルデータベース

ベクトルストアの作成方法:既存のベクトルストアを使用

ベクトルストア:OpenSearch Serverless

コレクションarn:出力プロパティのOpenSearchCollectionArn

ベクトルインデックス名:出力プロパティのIndexName

ベクトルフィールド名:「OpenSearch」→「Serverless:Collections」→「インデックス(bedrock-knowledge-base)」→ベクトルフィールド名の値

テキストフィールド名:text

Bedrock マネージドメタデータフィールド名:metadata

## task3
```
Striped Wool Knee-High Socks
```
