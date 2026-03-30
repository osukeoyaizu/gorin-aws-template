## task1
### RDSのオプショングループを作成
名前:任意

エンジン:mysql

メジャーエンジンバージョン:8.0

### オプションの追加
オプション名:MARIADB_AUDIT_PLUGIN

オプション設定の「SERVER_AUDIT_EVENTS*」の値を「QUERY_DML」

すぐに適用:Yes

### RDSを変更
ログのエクスポート:監査ログ

オプショングループ:作成したもの

すぐに適用

## task2
```
dev
```
