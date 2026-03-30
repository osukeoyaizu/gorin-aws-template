## OpenSearch API
### インデックス作成
**※typeをkeywordにしておくと可視化する際にフィールドとして選択できる**
```
PUT {index_name}
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "field1": { "type": "keyword" },
      "field2": { "type": "text" },
      "field3": { "type": "integer" },
      "created_at": { "type": "date", "format": "yyyy/MM/dd" }
    }
  }
}

```

### ドキュメント登録
```
POST {index_name}/_doc
{
  "field1": "value1",
  "field2": "value2",
  "field3": 123,
  "created_at": "2026/01/01"
}
```

#### IDを指定して作成
```
PUT {index_name}/_doc/{id}
{
  "field1": "value1",
  "field2": "value2",
  "field3": 123,
  "created_at": "2026/01/01"
}
```

### 全件取得
```
GET products/_search
```

### ドキュメント取得
```
GET {index_name}/_doc/{id}
```

### 検索
```
GET {index_name}/_search
{
  "query": {
    "match": {
      "field2": "keyword"
    }
  }
}
```


### 部分更新
```
POST {index_name}/_update/{id}
{
  "doc": {
    "field2": "updated value"
  }
}
```

### ドキュメント削除
```
DELETE {index_name}/_doc/{id}
```

### 条件削除
```
POST {index_name}/_delete_by_query
{
  "query": {
    "term": {
      "field1": "value1"
    }
  }
}
```
