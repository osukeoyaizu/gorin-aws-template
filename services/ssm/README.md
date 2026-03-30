## メンテナンスウィンドウ
### 定期的にEC2インスタンスのイメージを作成するオートメーションタスク
「Systems Manager」→「メンテナンスウィンドウ」→「Backup-MaintenanceWindow」→「アクション」→「オートメーションタスクの登録」

ターゲット:Task target not required

Instanceid:課題のEC2インスタンスID

cronで実行時間を設定する

## ドキュメント
### コマンド
#### WindowsとLinux両方に対応するドキュメント
```
---
schemaVersion: "2.2"
description: "Document to run simple commands on EC2 instances"
mainSteps:
- name: "ConfigureWindowsProxySettings"
  action: "aws:runPowerShellScript"
  precondition:
    StringEquals:
    - platformType
    - Windows
  inputs:
    runCommand:
    - "Write-Host 'Starting Windows configuration...'"
    - "Get-Date"
    - "Get-ComputerInfo | Select-Object WindowsProductName, OsArchitecture"
    - "Write-Host 'Windows configuration complete.'"

- name: "ConfigureLinuxProxySettings"
  action: "aws:runShellScript"
  precondition:
    StringEquals:
    - platformType
    - Linux
  inputs:
    runCommand:
    - "#!/bin/bash"
    - "echo 'Starting Linux configuration...'"
    - "date"
    - "uname -a"
    - "echo 'Linux configuration complete.'"
```

### オートメーション
#### パッチ適用、タグ付け
```
schemaVersion: '0.3'
description: SSM Automation to configure proxy settings, apply patches and set tags
assumeRole: arn:aws:iam::680797729568:role/LabStack-prewarm-bbf10584-0c8a-44-SSMAutomationRole-apNrJxxUDtft
parameters:
  InstanceId:
    description: List of Instances ID on which the automation will run.
    type: StringList
mainSteps:
  - name: tag_start
    action: aws:createTags
    nextStep: apply_patch
    isEnd: false
    inputs:
      ResourceIds:
        - '{{InstanceId}}'
      ResourceType: EC2
      Tags:
        - Value: postmigration_started
          Key: migration_status
  - name: apply_patch
    action: aws:runCommand
    nextStep: set_tag
    isEnd: false
    inputs:
      Parameters:
        Operation: Install
      InstanceIds:
        - '{{InstanceId}}'
      DocumentName: AWS-RunPatchBaseline
  - name: set_tag
    action: aws:createTags
    isEnd: true
    inputs:
      ResourceIds:
        - '{{InstanceId}}'
      ResourceType: EC2
      Tags:
        - Value: postmigration_completed
          Key: migration_status

```
※ オートメーションのパラメータを渡すEventBridgeルールの入力トランスフォーマー
```
{
  "instanceid": "$.detail.requestParameters.resourcesSet.items[*].resourceId"
}
```


## SSM Agentをインストール
### Linux
https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/hybrid-multicloud-ssm-agent-install-linux.html
```
mkdir /tmp/ssm
curl https://amazon-ssm-region.s3.region.amazonaws.com/latest/linux_amd64/ssm-setup-cli -o /tmp/ssm/ssm-setup-cli
sudo chmod +x /tmp/ssm/ssm-setup-cli
sudo /tmp/ssm/ssm-setup-cli -register -activation-code "a{ctivation-code}" -activation-id "{activation-id}" -region "{region}"
```

### Windows
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

## ハイブリッドアクティベーション
### Windows
https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/hybrid-multicloud-ssm-agent-install-windows.html
```
[System.Net.ServicePointManager]::SecurityProtocol = 'TLS12'
$code = "{activation-code}"
$id = "{activation-id}"
$region = "{region}"
$dir = $env:TEMP + "\ssm"
New-Item -ItemType directory -Path $dir -Force
cd $dir
(New-Object System.Net.WebClient).DownloadFile("https://amazon-ssm-$region.s3.$region.amazonaws.com/latest/windows_amd64/ssm-setup-cli.exe", $dir + "\ssm-setup-cli.exe")
./ssm-setup-cli.exe -register -activation-code="$code" -activation-id="$id" -region="$region"
Get-Content ($env:ProgramData + "\Amazon\SSM\InstanceData\registration")
Get-Service -Name "AmazonSSMAgent"
```


## Patch Manager
### スキャンとインストール
スキャン・・・インスタンスのパッチ適用状況を確認

インストール・・・不足しているパッチを実際に適用

#### 手順
SystemsManager → パッチマネージャー → 概要から開始 → 今すぐパッチ適用

パッチ適用操作:スキャンとインストール

インスタンスタグを指定(キー:Project,値:NewApp)

ログストレージ:出力プロパティのApplicationLogBucket
