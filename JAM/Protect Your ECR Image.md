## task1
ビルドプロジェクト(pyei-challenge-build)のサービスロールARNを回答する

## task2
ECRのリソースポリシー編集
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "new statement",
      "Effect": "Deny",
      "Principal": "*",
      "Action": ["ecr:PutImage"],
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": [
            "arn:aws:iam::{account-id}:role/service-role/pyei-challenge-codebuild-service-role"
          ]
        }
      }
    }
  ]
}
```

## task3
CodePipeline(pyei-challenge-pipeline)の変更をリリースする
