## 透明性・ガバナンス・責任あるAI運用
モデルカード・・・モデルの詳細情報を文書化し、透明性・説明責任を確保する

モデルダッシュボード・・・モデルのライフサイクル全体を可視化・管理するための統合ビュー


## Canvas
### データの前処理
#### CanvasのTabularを使用
SageMaker-AI → Canvas → Data Wrangler → Import and prepare → Tabular

#### s3からデータインポート
Select a data source → S3 → データファイル → import

#### 欠損値補完
Add transform → Handle missing → input columns → Select all

#### 重複削除
Add transform → Manage rows → Transform → Drop duplicates

#### s3にエクスポートする
Export → Export data to Amazon S3 → S3パス → Export

### 予測分析モデル作成
「My Models」→「New model」→「任意のモデル名を入力 & Predictive analysisを選択」→「Create」→「使用するデータセット」

Select a column to predict:予測する例を選択する

不必要な列のチェックを外す

### モデルをデプロイする
適切なパラメータを選択してデプロイする

## バッチ変換ジョブ
### 推論するデータ
- ラベル列不要(特徴量の列のみ)

### Pythonコード
'boto3/create_transform_job' を参照する

