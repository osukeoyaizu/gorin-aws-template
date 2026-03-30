## 感情分析ジョブの結果をRedshiftにインポート
### テーブル作成クエリ
```
CREATE TABLE your_table_name (
    file VARCHAR(256),
    line VARCHAR(256),
    sentiment VARCHAR(256),
    sentimentscore SUPER
);
```
### データインポート
```
copy your_table_name
from '<ジョブで作成されたjsonファイルのs3パス>'
iam_role 'IAMARN' 
json 'auto ignorecase';
```
