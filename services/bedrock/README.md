## データソースID取得(Redshift)
```
aws bedrock-agent list-data-sources --knowledge-base-id {KNOWLEDGE_BASE_ID} --region {REGION}
```

## ナレッジベースのIAM許可
※IAMR:の後をナレッジベースのロール名に変更して実行する
```
CREATE USER "IAMR:AmazonBedrockExecutionRoleForKnowledgeBase_qkbuc" WITH PASSWORD DISABLE;
GRANT USAGE ON SCHEMA public TO "IAMR:AmazonBedrockExecutionRoleForKnowledgeBase_qkbuc";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "IAMR:AmazonBedrockExecutionRoleForKnowledgeBase_qkbuc";
```

## プレイグラウンド
### チャット/テキスト
#### モデル
Nova LiteやTitan Text G1など

#### Maximum output tokens
意味:モデルが生成する最大トークン数（単語や記号の単位）

役割:出力の長さを制限する

#### Temperature
意味:生成のランダム性を制御するパラメータ

確率の低い単語をどれくらい許容するか（全体のランダム性）

役割:

- 低い値（0.0～0.3） → 決定的で一貫性のある回答（事実重視）

- 高い値（0.7～1.0） → 創造的で多様な回答（アイデア出しや文章生成向き）


#### Top-p
意味:確率分布の上位pの範囲で次のトークンを選択

候補の範囲をどこまで広げるか（確率上位の集合）

役割:
- 低い値（0.1～0.3） → より決定的、予測可能な回答
- 高い値（0.8～1.0） → 多様性を重視、創造的な回答

### 画像/動画
#### モデル
Nova Canvasなど

#### Prompt strength
生成結果に対して入力したプロンプトの影響度をどれくらい強く反映するかを調整するパラメータ


## ガードレール
### プロンプトインジェクション対策
プロンプト攻撃フィルターを有効化

### 回答が正しい参照情報に基づいているか検証
グラウンディングチェックを有効化する
