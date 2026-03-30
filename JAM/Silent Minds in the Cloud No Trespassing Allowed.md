## task1
Lambda関数(JamVPCLambda)をVPCに配置する

## task2
bedrock-runtimeのVPCエンドポイントを作成する

## task3
VPCエンドポイントのポリシー編集
```
{
	"Statement": [
		{
			"Action": "bedrock:InvokeModel",
			"Effect": "Allow",
			"Principal": "*",
			"Resource": "arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0"
		}
	]
}
```
