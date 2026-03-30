## エージェントの設定
### 前提条件
IAMにLambdaへのアクセス権を付与しておく
### エージェント向けの指示
```
あなたは「ダイナモ君」という名前のバーチャルアシスタントです。あなたの役割は、ユーザーがDynamoDBテーブルを作成・削除したいときにサポートすることです。

現在、利用できる機能は **create_table** と **delete_table** です。

**使用ルール：**
- ユーザーが「テーブルを作りたい」と言った場合は、テーブル名とパーティションキーを尋ねてください。
- ソートキーはオプションであることを伝えてください。
- 情報が不足している場合は捏造せず、フォローアップ質問をしてください。
- 成功時は「テーブル <tableName> を作成しました」と返してください。
- 失敗時は「テーブル作成に失敗しました」と返してください。

**関係ない質問への対応：**
このサービスは「DynamoDBテーブル管理のみ対応しています」と丁寧に伝えてください。
```
### エージェントを編集してアクショングループ追加
名前:任意

Lambda関数:{DynamoDB操作用Lambda}

アクショングループで「APIスキーマで定義」→「インラインスキーマエディタで定義」

以下のインラインスキーマを設定する
```

openapi: 3.0.0
info:
    title: DynamoDB Table Management API
    version: 1.0.0
    description: API for creating and deleting DynamoDB tables.
paths:
    /createTable:
        post:
            summary: Create a new DynamoDB table.
            description: Creates a DynamoDB table with the specified name and key schema.
            operationId: createTable
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      tableName:
                        type: string
                        description: Name of the DynamoDB table to create.
                      partitionKey:
                        type: string
                        description: Partition key name for the table.
                      sortKey:
                        type: string
                        description: Sort key name for the table (optional).
                    required:
                      - tableName
                      - partitionKey
            responses:
                '200':
                    description: Successfully created DynamoDB table.
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                  message:
                                    type: string
                                  tableArn:
                                    type: string
                '400':
                    description: Bad request. Missing or invalid parameters.

    /deleteTable:
        post:
            summary: Delete a DynamoDB table.
            description: Deletes the specified DynamoDB table.
            operationId: deleteTable
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      tableName:
                        type: string
                        description: Name of the DynamoDB table to delete.
                    required:
                      - tableName
            responses:
                '200':
                    description: Successfully deleted DynamoDB table.
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                  message:
                                    type: string
                '400':
                    description: Bad request. Missing or invalid parameters.

```

## Lambdaの設定
### リソースポリシーを設定
プリンシパル:bedrock.amazonaws.com

アクション:lambda:InvokeFunction
