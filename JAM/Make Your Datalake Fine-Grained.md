## task1
「Lake Formation」→「Databases」→「jam_covid_db」→「Edit」→「Use only IAM access control for new tables in this database」のチェックを外す

「Lake Formation」→「Data permissions」→プリンシパルにAWSLabsがつくもの以外を削除する

## task2
WorkgroupをAmazonAthenaLakeFormationにして保存されたクエリを全て実行する

作成した3つのテーブルの合計レコード数を回答する
```
107202
```

## task3
### 権限付与
IAMロール:jam-lfuser-role

テーブル:us_state_vaccination

Table permissions:Select

## task4
### データフィルター作成
名前:任意

Filterrows:location='Japan' 

### 権限付与
IAMロール:jam-lfuser-role

テーブル:world_vaccinations_by_manufacture

データフィルター:作成したもの

Table permissions:Select

## task4
### LF-Tags作成
Key:sensitivity

Values:High,Normal

### スキーマ編集
world_vaccinationsテーブルのカラム(country, iso_code, date, daily_vaccinations, daily_vaccinations_per_million)にLF-TagsのNormalを設定する

### 権限付与
IAMロール:jam-lfuser-role

LF-Tags or catalog resources:Resources matched by LF-Tags (recommended)

Key:sensitivity

Values:Normal

テーブル:world_vaccinations

Table permissions:Select

