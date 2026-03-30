## task1
### バージョニング設定
```
aws s3api put-bucket-versioning --bucket <バケット名> --versioning-configuration Status=Enable
```

### ライフサイクルルール設定(intelligent-tiering.json)
```
{
    "Rules": [
        {
            "ID": "IntelligentTieringTransition",
            "Prefix": "",
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 0,
                    "StorageClass": "INTELLIGENT_TIERING"
                }
            ]
        }
    ]
}
```

### ライフサイクルルール設定(CLI)
```
aws s3api put-bucket-lifecycle-configuration --bucket <バケット名> --lifecycle-configuration file://intelligent-tiering.json
```


## task2
**RDSをマルチAZに変換してすぐに適用する**

## task3
### Matchesでインデックス作成
インデックス名: GameDurationIndex

パーティションキー: gameDuration (数値)

属性投影:

投影タイプ: INCLUDE

投影された属性を 2 つ作成します。

属性名: championId

属性名: gameMode

## task4
**Redshiftのクエリエディタに接続する**
```
COPY high_diamond_ranked_10min FROM 's3://games-easy-storage-redshift-692182299394-us-west-2/high_diamond_ranked_10min.csv'
iam_role 'arn:aws:iam::692182299394:role/JamRedshiftRole'
CSV
IGNOREHEADER 1
DATEFORMAT 'auto';
```
