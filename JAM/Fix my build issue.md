## task1
CodeBuildに紐づくロール(challenge-codebuild-role)のポリシー(CodeBuild-Policy)に以下のステートメントを追加する
```
{
    "Sid": "Statement1",
    "Effect": "Allow",
    "Action": [
        "s3:*",
        "ecr:*",
        "kms:*"
    ],
    "Resource": [
        "*"
    ]
}
```
