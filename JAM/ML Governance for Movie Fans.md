## task1
「SageMaker AI」→「ガバナンス」→「モデルカード」

### モデルカード設定項目
モデルカード名:Movie-Revenue-Model-Card

モデルカードのステータス:承認済み

このモデルはAWSリソースです:チェックをつける

モデル名:Movie-Revenue-Predictor-Model (モデルの詳細を検索をクリック)

問題のタイプ:線形回帰

アルゴリズムタイプ:AdaBoost

## task2
「SageMaker AI」→「ガバナンス」→「モデルダッシュボード」→「Movie-Revenue-Predictor-Model」

### アラートを編集
アラートするデータポイント:2

評価期間:3

## task3
s3バケット(movie-revenue-artifacts-[account-id])のAmazon EventBridgeをオンにする

### EventBridgeルール作成
名前:任意

#### イベントパターン
```
{
  "source": ["aws.s3"],
  "detail-type": ["Object Access Tier Changed", "Object ACL Updated", "Object Created", "Object Deleted", "Object Restore Completed", "Object Restore Expired", "Object Restore Initiated", "Object Storage Class Changed", "Object Tags Added", "Object Tags Deleted"]
}
```

ターゲット:Step Functions ステートマシン

ロール:movie_revenue_eventbridge_role
