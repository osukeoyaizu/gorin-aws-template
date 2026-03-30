## Evaluate Data Quality
### カラムの値をチェックするルール
```
Rules = [
    ColumnValues "qty" > 0
]
```
※ メトリクスを使用してアラームを設定できる

## 加速クロール
### 手順
S3イベント通知の設定でSQSを設定する

Crawlerの「Data source」→「Crawl based on events」でSQSのARNを指定する


## ジョブにモジュールインポート
### ジョブパラメータに以下のように追加
--additional-python-modules	scikit-learn
#### 複数追加したい場合
scikit-learn==1.4.2,pandas==2.2.2,pyarrow==15.0.2,numpy==1.26.4,scipy==1.12.0,joblib==1.3.2,threadpoolctl==3.4.0



## ジョブをVPC内で動かす方法
- Connections作成
    - Network
        - VPC選択
        - サブネット選択
        - セキュリティグループ選択

- ジョブ設定
    - Job details
        - Advanced properties
            - Connections
