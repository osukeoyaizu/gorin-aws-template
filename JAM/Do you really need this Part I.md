## task1
プライベートVPC内のEC2にセッションマネージャーで接続できるようにする

EC2インスタンスにIAMロール「INSTANCE_ROLE」をアタッチする

セッションマネージャー接続に必要なVPCエンドポイント3つ(ssm,ssmmessages,ec2messages)を作成する

セッションマネージャーでEC2に接続する

### challenge.txtの内容を確認する
```
sudo su -
cat /challenge.txt
```

### ファイルの中の指示に従う
```
aws s3 cp s3://<s3バケット>/flag.txt ~/flag.txt --region=us-west-2
cat ~/flag.txt
```

