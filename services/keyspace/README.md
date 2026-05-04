## クエリ操作
### 最初に実行
```
CONSISTENCY LOCAL_QUORUM;
```
### INSERT
```
INSERT INTO table1 (id, name) VALUES (1, 'name02');
```

### TTL付きで登録
```
INSERT INTO table1 (id, name) VALUES (1, 'name02') USING TTL 10;
```