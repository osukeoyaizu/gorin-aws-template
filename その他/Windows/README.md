## コマンド
### Windowsのパスワードをリセットする
```
net user <ユーザー名> <パスワード>
```

### ポート確認
```
sudo netstat -tulnp | grep LISTEN
```

### 暗号化ツールで出力されたHexデータをバイナリに戻す
```
certutil -decodehex Output.txt output.bin
```

### GIF作成
```
ffmpeg -framerate 10 -pattern_type glob -i "*.jpg" aws.gif -y
cp aws.gif /var/www/html/
```

## SSM Agentに登録できない場合の対処法
### SSM Agentを再起動
```
Restart-Service AmazonSSMAgent
```

### 「DNSサーバーのアドレスを自動的に取得する」に変更する
```
ncpa.cpl
```

### ルーティングテーブルの確認
```
route print
```

### ルートの編集
```
route DELETE 169.254.169.254
route -p ADD 169.254.169.254 MASK 255.255.255.255 {Subnet default Gateway IP}
```

### プロキシ設定変更
```
netsh winhttp show proxy netsh winhttp reset proxy
```

### ファイアウォール
```
wf
```
→拒否ルールを削除する

### 時刻同期
```
W32tm /resync /force
```

## メタデータ取得
```
iwr -url 'http://169.254.169.254/latest/meta-data/'
```


## EC2Lunch
https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/ec2launch-download.html
### インストール
```
mkdir $env:USERPROFILE\Desktop\EC2Launch
$Url = "https://s3.amazonaws.com/ec2-downloads-windows/EC2Launch/latest/EC2-Windows-Launch.zip"
$DownloadZipFile = "$env:USERPROFILE\Desktop\EC2Launch\" + $(Split-Path -Path $Url -Leaf)
Invoke-WebRequest -Uri $Url -OutFile $DownloadZipFile
$Url = "https://s3.amazonaws.com/ec2-downloads-windows/EC2Launch/latest/install.ps1"
$DownloadZipFile = "$env:USERPROFILE\Desktop\EC2Launch\" + $(Split-Path -Path $Url -Leaf)
Invoke-WebRequest -Uri $Url -OutFile $DownloadZipFile
& $env:USERPROFILE\Desktop\EC2Launch\install.ps1
```

### 次回起動時に実行
```
C:\ProgramData\Amazon\EC2-Windows\Launch\Scripts\InitializeInstance.ps1 -Schedule
```

## Windowsのレジストリから特定のポリシー設定を削除
```
Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "WUServer"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "WUStatusServer"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "UseWUServer"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "DoNotConnectToWindowsUpdateInternetLocations"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "SetDisableUXWUAccess"
```

## Session Manager Plugin
### インストール
https://docs.aws.amazon.com/systems-manager/latest/userguide/install-plugin-windows.html

### 認証情報を取得
```
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance/
```

### 認証情報を設定
```
SET AWS_ACCESS_KEY_ID=
SET AWS_SECRET_ACCESS_KEY=
SET AWS_SESSION_TOKEN= 
```

### プライベートインスタンスへのセッションマネージャー接続を確立
```
aws ssm start-session --target {private-instance-id} --document-name AWS-StartPortForwardingSession --parameters portNumber="3389",localPortNumber="56789" --region {aws-region}
```
RDPでコンピュータ名をlocalhost:56789、資格情報を入力して接続する




