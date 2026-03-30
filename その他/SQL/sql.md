## SQL比較一覧（MySQL / PostgreSQL / Oracle）

---

### 1. データベース一覧・スキーマ一覧

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **データベース一覧** | `SHOW DATABASES;` | `\l` または `SELECT datname FROM pg_database;` | OracleはDBは1つ。`SELECT name FROM v$database;` |
| **スキーマ一覧** | `SELECT schema_name FROM information_schema.schemata;` | `\dn` または `SELECT schema_name FROM information_schema.schemata;` | `SELECT username FROM dba_users;` |

---

### 2. テーブル一覧

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **テーブル一覧** | `SHOW TABLES;` | `\dt` または `SELECT tablename FROM pg_tables WHERE schemaname='public';` | `SELECT table_name FROM user_tables;` |
| **全スキーマのテーブル一覧** | `SELECT table_schema, table_name FROM information_schema.tables;` | `SELECT schemaname, tablename FROM pg_tables;` | `SELECT owner, table_name FROM all_tables;` |

---

### 3. カラム一覧（テーブル定義）

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **カラム一覧** | `DESCRIBE table;` / `SHOW COLUMNS FROM table;` | `\d table` / `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='table';` | `DESC table;` / `SELECT column_name, data_type FROM user_tab_columns WHERE table_name='TABLE';` |

---

### 4. データベース切り替え（USE）

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **データベース切り替え** | `USE dbname;` | `\c dbname` | OracleはDB切替なし（スキーマ切替：`ALTER SESSION SET CURRENT_SCHEMA = schema;`） |

---

### 5. SELECT / INSERT / UPDATE / DELETE

#### SELECT
| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **SELECT** | `SELECT * FROM table;` | `SELECT * FROM table;` | `SELECT * FROM table;` |

#### INSERT
| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **INSERT** | `INSERT INTO table (col1, col2) VALUES (1, 'A');` | `INSERT INTO table (col1, col2) VALUES (1, 'A');` | `INSERT INTO table (col1, col2) VALUES (1, 'A');` |

#### UPDATE
| 操作 | MySQL / PostgreSQL / Oracle 共通 |
|------|----------------------------------|
| **UPDATE** | `UPDATE table SET col = 'value' WHERE id = 1;` |

#### DELETE
| 操作 | MySQL / PostgreSQL / Oracle 共通 |
|------|----------------------------------|
| **DELETE** | `DELETE FROM table WHERE id = 1;` |

---

### 6. テーブル作成・削除（CREATE / DROP）

#### CREATE TABLE（共通）
```sql
CREATE TABLE sample (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  created_at TIMESTAMP
);
```

※Oracleは `VARCHAR2` を使うことが多い。

#### DROP TABLE（共通）
```sql
DROP TABLE table;
```

---

### 7. テーブル構造変更（ALTER TABLE）

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **カラム追加** | `ALTER TABLE table ADD column VARCHAR(100);` | 同左 | 同左 |
| **カラム削除** | `ALTER TABLE table DROP COLUMN column;` | 同左 | 同左 |
| **カラム名変更** | `ALTER TABLE table CHANGE old new VARCHAR(100);` | `ALTER TABLE table RENAME COLUMN old TO new;` | `ALTER TABLE table RENAME COLUMN old TO new;` |

---

### 8. インデックス

#### インデックス一覧

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **インデックス一覧** | `SHOW INDEX FROM table;` | `\di` / `SELECT * FROM pg_indexes WHERE tablename='table';` | `SELECT index_name FROM user_indexes WHERE table_name='TABLE';` |

#### インデックス作成（共通）
```sql
CREATE INDEX idx_name ON table (column);
```

---

### 9. 行制限（LIMIT / ROWNUM）

| 操作 | MySQL | PostgreSQL | Oracle |
|------|--------|-------------|---------|
| **先頭10件取得** | `SELECT * FROM table LIMIT 10;` | `SELECT * FROM table LIMIT 10;` | `SELECT * FROM table WHERE ROWNUM <= 10;` |

---

### 10. トランザクション

| 操作 | SQL |
|------|------|
| **開始** | `BEGIN;` |
| **コミット** | `COMMIT;` |
| **ロールバック** | `ROLLBACK;` |

---

