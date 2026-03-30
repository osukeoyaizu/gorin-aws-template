## task1
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

## task2
ハイブリッドアクティベーションをIAMロール(Production-SSMServiceRole)を指定して作成し、Activation IDを回答する

## task3
RDPでインスタンスに接続する

PowerShellをAdministrator権限で開く

コントロールパネルからSSM Agentをアンインストールする

### SM Agentをインストールする
https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/manually-install-ssm-agent-windows.html
```
[System.Net.ServicePointManager]::SecurityProtocol = 'TLS12'
$progressPreference = 'silentlyContinue'
Invoke-WebRequest `
    https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/windows_amd64/AmazonSSMAgentSetup.exe `
    -OutFile $env:USERPROFILE\Desktop\SSMAgent_latest.exe
Start-Process `
    -FilePath $env:USERPROFILE\Desktop\SSMAgent_latest.exe `
    -ArgumentList "/S" `
    -Wait
rm -Force $env:USERPROFILE\Desktop\SSMAgent_latest.exe
Restart-Service AmazonSSMAgent
```

### ハイブリッドアクティベーションを有効化する
https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/hybrid-multicloud-ssm-agent-install-windows.html
```
[System.Net.ServicePointManager]::SecurityProtocol = 'TLS12'
$code = "<activation-code>"
$id = "<activation-id>"
$region = "<region>"
$dir = $env:TEMP + "\ssm"
New-Item -ItemType directory -Path $dir -Force
cd $dir
(New-Object System.Net.WebClient).DownloadFile("https://amazon-ssm-$region.s3.$region.amazonaws.com/latest/windows_amd64/ssm-setup-cli.exe", $dir + "\ssm-setup-cli.exe")
./ssm-setup-cli.exe -register -activation-code="$code" -activation-id="$id" -region="$region"
Get-Content ($env:ProgramData + "\Amazon\SSM\InstanceData\registration")
Get-Service -Name "AmazonSSMAgent"
```
