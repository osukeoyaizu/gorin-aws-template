## S3からCSVファイルを読み込み、Spark DataFrameに変換
### CSVデータ
```
game_id,player1,player2,winner,
1,Alice,Bob,Alice
2,Alice,Bob,Bob
3,Alice,Bob,Alice
```
### 変換コード
```
import sys

input_path = "s3://bucket_name/games_data.csv"
my_data = spark.read.option("inferSchema", "true").option("header", "true").csv(input_path)
my_data.count()
```

## DataFrameをRDDに変換
```
my_rdd = my_data.rdd
mapped_rdd = my_rdd.map(lambda row: (row.winner, 1))
# → [("Alice", 1), ("Bob", 1), ("Alice", 1)]
mapped_rdd.countByKey()
# → {"Alice": 2, "Bob": 1}

```

## groupByKey
```
# mapped_rdd = [("Alice", 1), ("Bob", 1), ("Alice", 1)]
grouped_rdd = mapped_rdd.groupByKey()
# → [("Alice", [1, 1]), ("Bob", [1])]
reduced_rdd = grouped_rdd.map(lambda row: (row[0], sum(row[1])))
# → [("Alice", 2), ("Bob", 1)]
collected_dict = reduced_rdd.collect() # RDDをPythonリストに変換
```

## reduceByKey
```
reduced_rdd = mapped_rdd.reduceByKey(lambda a, b: a + b)
# → [("Alice", 2), ("Bob", 1)]
collected_dict = reduced_rdd.collect() # RDDをPythonリストに変換
```
