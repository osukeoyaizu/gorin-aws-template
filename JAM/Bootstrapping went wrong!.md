## task1
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

インスタンスのパブリックIPを回答する

## task2
RDP接続し、以下のコマンドを実行する
```
route DELETE 169.254.169.254
route -p ADD 169.254.169.254 MASK 255.255.255.255 {Subnet default Gateway IP}
Restart-Service AmazonSSMAgent
```
{Subnet default Gateway IP}・・・route printコマンドを実行して、最初のネットワーク宛先 0.0.0.0 のゲートウェイIP


以下のコマンドを実行して検証ボタンを何度かクリックする
```
(tnc 169.254.169.254 -Port 80 | Select-Object -Property TcpTestSucceeded)
```
## task3
### scripts.ps1ファイルを作成し、C:\に保存する
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

### scripts.ps1ファイルを実行する
```
cd 'C:\'
.\scripts.ps1
```

### 以下のコマンドを実行
```
C:\ProgramData\Amazon\EC2-Windows\Launch\Scripts\InitializeInstance.ps1 -Schedule
```

**※クリアにならない場合はコントロールパネルから削除し、再インストールしてみる**

## task4
```
echo hoge >  C:\validate.ps1
```
