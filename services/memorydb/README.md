## ACL
```
on ~* &* +@all
```
### ① `on` ：ユーザーを有効にする
```
on
```
- この ACL ユーザーを **有効化** する指定です
- 無効にしたい場合は `off`


### ② `~*` ：アクセスできるキーの範囲
```
~*
```
- `~` は **キー名のパターン指定**
- `*` は **すべて** を意味します

#### 例
| 指定 | 意味 |
|---|---|
| `~user:*` | `user:` で始まるキーのみ許可 |
| `~cache:*` | キャッシュ用キーのみ |

### ③ `&*` ：Pub/Sub チャネルの範囲
```
&*
```
- `&` は Pub/Sub の **チャネル名**
- `*` は **すべて**

### ④ `+@all` ：実行可能なコマンド
```
+@all
```

- `+` は **許可**
- `@all` は **すべてのコマンドカテゴリ**
#### コマンドカテゴリの例

| カテゴリ | 内容例 |
|---|---|
| `@read` | GET / EXISTS など |
| `@write` | SET / DEL / INCR |
| `@admin` | ACL / CONFIG |
| `@dangerous` | FLUSHALL / KEYS |


## よくある実用的な ACL 例

### アプリ用（キーを限定）

```
on ~app:* &* +@read +@write
```

### キャッシュ専用

```
on ~cache:* +get +set +del
```

### Pub/Sub 専用
```
on &events:* +publish +subscribe
```



## 接続コマンド(ユーザー使用)
```
curl -O https://www.amazontrust.com/repository/AmazonRootCA1.pem
redis6-cli -c -h {エンドポイント}   -p 6379   --tls   --cacert AmazonRootCA1.pem --user {ユーザー名} -a '{パスワード}'
```

