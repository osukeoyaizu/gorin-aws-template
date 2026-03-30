## RDSのデータを分析

**QuickSight用のセキュリティグループを作成し、RDSのセキュリティグループで許可する**

### QuickSightに紐づくロールに権限を追加する
```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
```
**※SecretsManagerの権限も必要**

**VPC接続を作成しておく**

### CLIからデータソースを作成する
https://docs.aws.amazon.com/cli/latest/reference/quicksight/create-data-source.html
```
aws quicksight create-data-source \
    --aws-account-id <account-id> \
    --data-source-id <ランダムな値> \
    --name oyaizu-aurora \
    --type MYSQL \
    --data-source-parameters '{"RdsParameters": {"InstanceId":"<DB 識別子>","Database":"<データベース名>"}}' \
    --credentials '{"SecretArn":"<SecretsManagerのARN>"}' \
    --vpc-connection-properties VpcConnectionArn=<QuickSightで作成したVPC接続のARN> \
    --permissions '[
            {
                "Principal": "arn:aws:quicksight:<REGION>:140083316867:user/default/<QuickSightのユーザー名>",
                "Actions": [
                    "quicksight:UpdateDataSourcePermissions",
                    "quicksight:DescribeDataSourcePermissions",
                    "quicksight:PassDataSource",
                    "quicksight:DescribeDataSource",
                    "quicksight:DeleteDataSource",
                    "quicksight:UpdateDataSource"
                ]
            }
        ]' 

```

**作成されたデータソースからデータセットを作成して分析する**
