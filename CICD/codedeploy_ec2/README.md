## 前提条件
Blue用,Green用のターゲットグループを作成しておく

## 起動テンプレートのユーザーデータ
```
#!/bin/bash

### CodeDeploy導入の事前準備
sudo yum install ruby -y
sudo yum install wget -y

### CodeDeployインストーラーのダウンロード
cd /home/ec2-user
wget https://aws-codedeploy-ap-northeast-1.s3.ap-northeast-1.amazonaws.com/latest/install

### CodeDeployのインストール
chmod +x ./install
sudo ./install auto

### httpdのインストールおよび起動
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

## CodeDeployに必要な権限
AWSCodeDeployRole

AutoScalingFullAccess
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole",
                "ec2:RunInstances",
                "ec2:CreateTags"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
## EC2に必要な権限
AmazonEC2RoleforAWSCodeDeploy

AmazonS3FullAccess(ソースがS3の場合)
