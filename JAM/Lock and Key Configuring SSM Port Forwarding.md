## task1
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

## task2
**リモートデスクトップで接続したWindowsにCLIとSession Manager Pluginをインストールする**

Latest AWS CLI for Windows

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions

Session Manager Plugin for Windows

https://docs.aws.amazon.com/systems-manager/latest/userguide/install-plugin-windows.html

**認証情報を取得するために以下のURLに接続先のブラウザでアクセスする**
```
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance/
```

**上記のリンクから一時的な資格情報を取得し、PowerShell を使用して次のコマンドを実行して同じものを構成**
```
SET AWS_ACCESS_KEY_ID=
SET AWS_SECRET_ACCESS_KEY=
SET AWS_SESSION_TOKEN= 
```

**確認**
```
aws sts get-caller-identity
```


**プライベートインスタンスへのセッションマネージャー接続を確立**
```
aws ssm start-session --target {private-instance-id} --document-name AWS-StartPortForwardingSession --parameters portNumber="3389",localPortNumber="56789" --region {aws-region}
```

**接続先のWindowsからコンピュータ名をlocalhost:56789、Bastion ホストと同じ RDP 資格情報を使用してログイン**

**プライベートEC2インスタンスのデスクトップにあるValidateAccessを実行する**



