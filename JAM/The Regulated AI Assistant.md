## task1
### AWS CLIでBedrockエージェントのIDを取得する
```
aws bedrock-agent list-agents
```

### キーポリシー
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Enable IAM User Permissions",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::<accout-id>:root"
			},
			"Action": "kms:*",
			"Resource": "*"
		},
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Principal": {
				"Service": "bedrock.amazonaws.com"
			},
			"Action": [
				"kms:Decrypt",
				"kms:Encrypt",
				"kms:GenerateDataKey"
			],
			"Resource": "*",
			"Condition": {
				"StringEquals": {
					"aws:SourceAccount": "<accout-id>"
				},
				"ArnLike": {
					"aws:SourceArn": "arn:aws:bedrock:<accout-id>:<region>:agent/<agent-id>"
				}
			}
		}
	]
}
```

## task2
### ガードレールの機密情報フィルターを編集(3つのPII Typeを選択してブロックする)
CREDIT_DEBIT_CARD_NUMBER

EMAIL

PHONE

## task3
### ガードレールの拒否トピックを追加する
名前:Investment Advice

定義:Investment advice is inquiries, guidance, or recommendations about the management or allocation of funds or assets with the goal of generating returns or achieving specific financial objectives.

サンプルフレーズ:Is investing in stocks better than bonds?

## task4
「Bedrock」→「設定」→モデル呼び出しのログ記録を有効化する

出力プロパティのLogBucketNameを選択する
