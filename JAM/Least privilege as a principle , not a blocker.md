## task1
### EventBridgeルール作成
名前:ec2statechangeevents

イベントパターン
```
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

ターゲット:Lambda(leastprivilegejam-create-tags)

## task2
### パラメータストア作成
名前:/abc/apps/tags

値
```
Department=Marketing
```

## task3
### ec2インスタンス起動
インスタンスタイプ:t2.micro

セキュリティグループ:default


## task4
### IAMポリシー(XYZusersPermissionBoundary)編集
```
{
  "Version": "2012-10-17",
  "Statement": [
 {
     "Action": [
         "ec2:DescribeInstances"
     ],
     "Resource": "*",
     "Effect": "Allow"
 },
 {
     "Action": [
         "ec2:StopInstances",
         "ec2:StartInstances"
     ],
     "Resource": "arn:aws:ec2:*:{account-id}:instance/*",
     "Effect": "Allow"
 },
  {
    "Action": "ec2:StopInstances",
    "Effect": "Deny",
    "Resource": "*",
    "Condition": {
      "StringEqualsIgnoreCase": {
        "aws:ResourceTag/Department": "Marketing"
     }
    }
   }
  ]
}
```
