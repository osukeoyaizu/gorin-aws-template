### VPC
- VPCフローログ
- プライベートサブネットのデフォルトルート
- VPCエンドポイント
- セキュリティグループ(全許可なし)
- リージョナルNATゲートウェイ
- タグ

### KMS
- キーポリシー
- キーローテーション
- タグ

### AWS Backup
- 暗号化(ボールト)
- バックアッププラン
  - RDS 
  - Aurora
  - DynamoDB
  - EC2
  - EFS
  - S3
  - Redshift

### S3
- ライフサイクルルール
- ストレージタイプ
- バージョニング
- 暗号化
  - SSE-KMS
- アクセスログ
- パブリックアクセスブロック
- リソースポリシー
- タグ

### API Gateway
- アクセスログ
- X-Ray
- WAF
- オーソライザ
- リソースポリシー
- CloudFront
- タグ

### Lambda
- パワーツール
- CloudWatch Application Signals and AWS X-Ray
- メモリサイズ
- 環境変数
- 暗号化(.zip, 環境変数)
- 例外処理(SQS)
- パワーチューニング(時間があれば)
- リソースポリシー
- バージョニング
- エイリアス
- タグ

### CloudFront
- HTTPS Only
- アクセスログ
- WAF
- タグ

### SecretsManager
- ローテーション
- 暗号化
- リソースポリシー
- タグ

### DynamoDB
- キャパシティ
- 削除保護
- 暗号化
- PITR
- オンデマンドバックアップ
- リソースポリシー
- タグ

### ALB
- アクセスログ
- 削除保護
- WAF
- タグ

### RDS(Aurora)
- マルチAZ
- 削除保護
- 暗号化
- ログ設定
- 自動バックアップ
- マイナーバージョン自動アップグレード
- オンデマンドバックアップ
- データベースユーザー(デフォルトのユーザーを使用しない)
- SecretsManager
- タグ

### EC2
- マルチAZ
- ALB
- EBS暗号化
- AutoScaling
  - ターゲット追跡ポリシー
- PublicIP自動割り当て無効
- AMI使用
- タグ


### ECR
- イミュータブル
- 暗号化
- ライフサイクルルール
- リソースポリシー
- 拡張スキャン
- タグ

### ECS
- マルチAZ
- Container Insights
- タスクログ
- 暗号化
- サービスのスケーリング
- PublicIP自動割り当て無効
- タグ

### EKS
- マルチAZ
- 暗号化
- 監査ログ
- Podログ
- Container Insights
- Karpenter
- Horizontal Pod Autoscaler
- タグ

### CloudWatch
- ログの保持期間
- ダッシュボード
  - Lambda
    - Duration
    - Errors
    - Throttles
  - DynamoDB
    - ConsumedReadCapacityUnits
    - ConsumedWriteCapacityUnits
  - EC2
    - CPUUtilization
    - DiskReadOps / DiskWriteOps
    - NetworkIn / NetworkOut
  - ECS
    - CPUUtilization
    - MemoryUtilization
  - EKS
    - CPU Utilization
    - Memory Utilization
  - CloudFront(ALB)
    - RequestCount
    - HTTPCode_Target_4XX_Count
    - HTTPCode_Target_5XX_Count
- アラーム

### SQS
- 暗号化
- デッドレターキュー
- タグ

### SNS
- 暗号化
- タグ

### CodeCommit
- 暗号化
- タグ

### DataStream
- キャパシティ
- 暗号化
- タグ

### DataFirehose
- タイムアウト(1分)
- 暗号化
- タグ

### ElastiCache
- マルチAZ
- 暗号化
- 転送中の暗号化
- タグ

### EFS
- マルチAZ
- ファイルシステムポリシー(転送時の暗号化)
- 暗号化
- タグ

### StepFunctions
- 暗号化
- ログ
- X-Ray
- バージョン
- エイリアス
- タグ

### Redshift
- マルチAZ
- 暗号化
- 監査ログ
- SecretsManager
- リソースポリシー
- タグ

### OpenSearch
- ライフサイクルルール
- マルチAZ
- リソースポリシー
- タグ

### Glue
- ジョブのリトライ処理
- タグ

### ParameterStore
- 暗号化
- intelligent
- タグ

### CloudFormation
- IaC管理

### その他
- Config
- CloudTrail
- GuardDuty
  - GuardDutyFindingExport
- Inspector
- Security Hub
- 不要なリソース削除