## task1
Lambda関数(myLambdaFunction)の環境変数の転送時、保管時の暗号化をする

## task2
Lambda関数に紐づくIAMロール(myLambdaFunctionExecutionRole)にインラインポリシー作成
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"kms:Decrypt",
				"kms:Encrypt"
			],
			"Resource": "<KMSキーARN>"
		}
	]
}
```

## task3
キーポリシーのDenyをAllowに変更する
