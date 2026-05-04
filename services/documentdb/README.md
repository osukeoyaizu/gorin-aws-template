## mongosh install
https://www.mongodb.com/ja-jp/docs/mongodb-shell/install/?operating-system=linux&linux-distribution=amazon&amazon-linux-version=amazon2023&msockid=01fba74f85906e4f199bb24384276f59

-  /etc/yum.repos.d/mongodb-org-8.2.repo
```
[mongodb-org-8.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/8.2/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-8.0.asc
```
```
sudo yum install -y mongodb-mongosh
```

## 接続
```
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
mongosh {エンドポイント}:27017 --tls --tlsCAFile global-bundle.pem --retryWrites=false --username {ユーザー名} --password {パスワード}
```


## 前提

- SQL のテーブル = MongoDB の **collection**
- SQL の行（row） = MongoDB の **document**
- サンプル collection 名: `orders`

---

## 基本操作の対応

| 処理内容 | SQL | MongoDB（mongosh） |
|---|---|---|
| 全件取得 | SELECT * | find() |
| 条件抽出 | WHERE | find({}) |
| 件数 | COUNT | countDocuments() |
| 合計 | SUM | $sum |
| グループ化 | GROUP BY | aggregate + $group |
| 並び替え | ORDER BY | sort() |
| 件数制限 | LIMIT | limit() |

---

## SELECT / FIND

### SQL

```sql
SELECT * FROM orders;
```

### mongosh

```js
db.orders.find()
```

---

## WHERE（条件指定）

### SQL

```sql
SELECT * FROM orders WHERE status = 'paid';
```

### mongosh

```js
db.orders.find({ status: "paid" })
```

### 比較演算子対応

| SQL | MongoDB |
|---|---|
| = | { field: value } |
| > | { field: { $gt: value } } |
| >= | { field: { $gte: value } } |
| < | { field: { $lt: value } } |
| IN | { field: { $in: [...] } } |

---

## COUNT（件数）

### SQL

```sql
SELECT COUNT(*) FROM orders;
```

### mongosh

```js
db.orders.countDocuments()
```

条件付き

```js
db.orders.countDocuments({ status: "paid" })
```

---

## SUM（合計）

### SQL

```sql
SELECT SUM(amount) FROM orders;
```

### mongosh

```js
db.orders.aggregate([
  { $group: { _id: null, totalAmount: { $sum: "$amount" } } }
])
```

---

## GROUP BY

### SQL

```sql
SELECT status, SUM(amount)
FROM orders
GROUP BY status;
```

### mongosh

```js
db.orders.aggregate([
  { $group: { _id: "$status", totalAmount: { $sum: "$amount" } } }
])
```

---

## GROUP BY + COUNT

### SQL

```sql
SELECT status, COUNT(*)
FROM orders
GROUP BY status;
```

### mongosh

```js
db.orders.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
])
```

---

## WHERE + GROUP BY

### SQL

```sql
SELECT status, SUM(amount)
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY status;
```

### mongosh

```js
db.orders.aggregate([
  { $match: { created_at: { $gte: ISODate("2024-01-01") } } },
  { $group: { _id: "$status", totalAmount: { $sum: "$amount" } } }
])
```

---

## ORDER BY

### SQL

```sql
SELECT * FROM orders ORDER BY amount DESC;
```

### mongosh

```js
db.orders.find().sort({ amount: -1 })
```

---

## LIMIT

### SQL

```sql
SELECT * FROM orders LIMIT 10;
```

### mongosh

```js
db.orders.find().limit(10)
```