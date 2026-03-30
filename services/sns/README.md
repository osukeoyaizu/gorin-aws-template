
## よく使うテンプレ（Message Attributes）

### 1) 環境ごとのサブスク振り分け（OR）
```json
{
  "env": ["prod", "stg"]
}
```
- `env` が `prod` または `stg` のメッセージだけを受信（**OR**）。

### 2) イベント種別の多値（OR）
```json
{
  "eventType": ["OrderCreated", "OrderUpdated", "OrderCancelled"]
}
```

### 3) 文字列のプレフィックス一致（prefix）
```json
{
  "orderId": [ { "prefix": "ord-" } ]
}
```
- `ord-12345` などを許可。複数プレフィックスを並べれば **OR**。

### 4) ブラックリスト（anything-but）
```json
{
  "region": [ { "anything-but": ["cn-north-1", "cn-northwest-1"] } ]
}
```
- 指定リージョン**以外**を許可。

### 5) 存在チェック（exists）
```json
{
  "traceId": [ { "exists": true } ]
}
```
- `traceId` 属性が**存在する**メッセージのみ受信。存在しないメッセージを除外。

### 6) 数値比較（Number 型属性）
```json
{
  "latencyMs": [ { ">": 100 }, { "<=" : 2000 } ]
}
```
- `latencyMs > 100` **かつ** `latencyMs <= 2000` を満たすもの（同じ属性内は **AND** で評価）。
- 使える演算子例: `=`, `>`, `>=`, `<`, `<=`, `{ "between": [min, max] }`

### 7) 属性間の AND 条件（複合）
```json
{
  "env": ["prod"],
  "eventType": ["OrderCreated", "OrderUpdated"],
  "priority": [ { ">=": 3 } ]
}
```
- **異なる属性同士は AND**。上記は `env=prod` **かつ** `eventType ∈ {OrderCreated, OrderUpdated}` **かつ** `priority >= 3`。

### 8) 値が *存在しない* ことを条件にする
```json
{
  "deprecatedFlag": [ { "exists": false } ]
}
```
- 属性が無い／未設定のメッセージだけを許可。

### 9) 文字列のホワイトリスト + 一部否定の組合せ
```json
{
  "service": ["billing", "order", { "anything-but": ["legacy"] } ]
}
```
- `billing` または `order`、または `legacy` 以外の任意の値。

### 10) 何もフィルターしない（全通し）
```json
{}
```
- フィルターポリシーを空にすると、**全メッセージを配信**。

---

## メッセージ本文（JSON）でのフィルタリング（Message Body）
メッセージ本文の JSON を対象にするには、`FilterPolicyScope=MessageBody` を設定します。ポリシー内では特殊キー `"aws:MessageBody"` を使い、ネストしたキーをドットで参照します。

> 例: 本文 `{ "env": "prod", "order": { "id": "ord-1", "amount": 5000, "tags": ["vip","first"] } }`

### 1) ネスト + 文字列一致 / prefix
```json
{
  "aws:MessageBody": {
    "env": ["prod"],
    "order.id": [ { "prefix": "ord-" } ]
  }
}
```

### 2) 数値比較（本文の数値）
```json
{
  "aws:MessageBody": {
    "order.amount": [ { ">": 1000 } ]
  }
}
```

### 3) 配列要素に対する一致（OR）
```json
{
  "aws:MessageBody": {
    "order.tags": ["vip", "priority"]
  }
}
```
- `order.tags` 配列の**いずれか**にマッチすれば許可。

### 4) 複合（AND）
```json
{
  "aws:MessageBody": {
    "env": ["prod"],
    "order.amount": [ { ">=": 1000 }, { "<=": 10000 } ],
    "order.tags": [ { "anything-but": ["blocked"] } ]
  }
}
```

---

## 送信側（Publish）での属性付与例（AWS CLI）
```bash
aws sns publish \
  --topic-arn arn:aws:sns:ap-northeast-1:123456789012:my-topic \
  --message '{"env":"prod","order":{"id":"ord-1","amount":1200}}' \
  --message-attributes '{
      "env": {"DataType":"String", "StringValue":"prod"},
      "eventType": {"DataType":"String", "StringValue":"OrderCreated"},
      "latencyMs": {"DataType":"Number", "StringValue":"150"}
  }'
```

---

## 実践 Tips / よくある落とし穴
- **Message Attributes と Message Body は別物**：本文で絞るなら `FilterPolicyScope=MessageBody` を忘れずに。
- **型に注意**：`Number` は数値比較、`String` は文字列演算（`prefix`, `anything-but`）。誤った型だとマッチしません。
- **同一属性内は AND**、配列要素は OR：`{"latencyMs": [ {">":100}, {"<=":2000} ]}` は両方満たす必要あり。
- **デフォルトはドロップ**：フィルタにマッチしないメッセージは**配信されません**（失敗ではなく“対象外”）。
- **SQS サブスク × RawDelivery**：SQS に配信する時、`RawMessageDelivery=true` にすると SNS ラッパー無しで本文が届き、属性も SQS Message Attributes として渡されます。
- **段階的導入**：最初は広め（空 or 緩い条件）→ CloudWatch メトリクスで配信件数を観察 → 条件を狭めるのが安全。

---

## すぐ使えるスニペット集（コピー用）

### Message Attributes 用
```json
{"env":["prod","stg"]}
```
```json
{"eventType":["OrderCreated","OrderUpdated","OrderCancelled"]}
```
```json
{"orderId":[{"prefix":"ord-"}]}
```
```json
{"region":[{"anything-but":["cn-north-1","cn-northwest-1"]}]}
```
```json
{"traceId":[{"exists":true}]}
```
```json
{"latencyMs":[{">":100},{"<=":2000}]}
```
```json
{"env":["prod"],"eventType":["OrderCreated","OrderUpdated"],"priority":[{">=":3}]}
```
```json
{"deprecatedFlag":[{"exists":false}]}
```
```json
{"service":["billing","order",{"anything-but":["legacy"]}]}
```
```json
{}
```

### Message Body 用（`FilterPolicyScope=MessageBody` 必須）
```json
{"aws:MessageBody":{"env":["prod"],"order.id":[{"prefix":"ord-"}]}}
```
```json
{"aws:MessageBody":{"order.amount":[{">":1000}]}}
```
```json
{"aws:MessageBody":{"order.tags":["vip","priority"]}}
```
```json
{"aws:MessageBody":{"env":["prod"],"order.amount":[{">=":1000},{"<=":10000}],"order.tags":[{"anything-but":["blocked"]}]}}
```
