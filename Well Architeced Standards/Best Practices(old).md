### AWSコストの最適化
- ライフサイクルルール
  - S3
  - ECR
  - OpenSearch
- s3のストレージタイプ
- CloudWatchLogsの保持期間


### セキュリティ要件
- IAM
- セキュリティグループ
- WAF
  - CloudFront
  - APIGateway
- リソースポリシー
  - ecr
- ローテーション
  - SecretsManager
  - KMS
- 暗号化
  - S3
    - SSE-KMS
  - RDS
  - Redshift
  - DynamoDB
  - ECR
  - EFS
  - CodeCommit
  - DataStream
  - DataFirehose
  - SecretsManager
  - ParameterStore
  - ElastiCache
- VPCエンドポイント
- ビューアープロトコル(Https)
- 環境変数を使用
  - Lambda
- Cognito
  - オーソライザ
- データベースユーザー(Adminを使用しない)
- GuardDuty
  - GuardDutyFindingExport 
- Inspector
  - Lambda標準スキャン
- Security Hub


### 信頼性・可用性要件
- タグ付け
- マルチAZ
  - EC2
  - ECS
  - EKS
  - RDS
  - Redshift
  - OpenSearch
- ALBの負荷分散
- スケーリング
- イミュータブル
- アクセスログの有効化
  - S3
  - ALB
  - CloudFront
  - APIGateway
  - VPCフローログ
  - RDSログ
  - Redshift監査ログ
  - タスク定義ログ
  - EKS Pod ログ
- バックアップ
  - AWS Backup
  - オンデマンドバックアップの作成
  - DynamoDB PITR


### 運用性要件
- 削除保護
  - rds
  - dynamodb
  - alb
- バージョン管理
  - s3
  - Lambda
  - StepFunctions
  - CodeCommit
- エイリアス
  - Lambda
- CloudTrail
- リトライ処理
  - Glueジョブ
- タイムアウト
  - DataFirehose(Lambda)


### パフォーマンス要件
- 読み込み/書き込みキャパシティー
  - 予測不能、短期間に高アクセス→オンデマンド
  - 緩やかにアクセス数増加→プロビジョンドのautoscaling
  - コストを抑える→プロビジョンド
- SQSデッドレターキュー
- CloudWatch
  - ダッシュボード
  - アラーム
  - ECS Container Insights
  - EKS Container Insights
- X-Rayトレーシング
  - APIGateway
  - Lambda
  - StepFunctions
- メモリの割り当て量を最適化
- 同時実行数
- パワーツール(Lambda)
- キャッシュの使用


