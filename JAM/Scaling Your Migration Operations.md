## task1
### SystemsManagerのドキュメント(ConfigureProxy)の新しいバージョンを作成する
**※作成後にデフォルトバージョンを変更する**
```
---
schemaVersion: "2.2"
description: "Document to configure proxy settings on Amazon EC2 instances"
mainSteps:
- inputs:
    runCommand:
    - "$proxy=\"http://proxy.acme.aws:3128\""
    - "$no_proxy_comma=\"169.254.169.254,ssm.eu-west-1.amazonaws.com,ec2.eu-west-1.amazonaws.com,ec2messages.eu-west-1.amazonaws.com\""
    - "$no_proxy = $no_proxy_comma.split(',') -join ';'"
    - "$serviceKey = \"HKLM:\\SYSTEM\\CurrentControlSet\\Services\\AmazonSSMAgent\""
    - "$keyInfo = (Get-Item -Path $serviceKey).GetValue(\"Environment\")"
    - "$proxyVariables = @(\"http_proxy=$proxy\", \"no_proxy=$no_proxy_comma\")"
    - "If($keyInfo -eq $null){"
    - "New-ItemProperty -Path $serviceKey -Name Environment -Value $proxyVariables\
      \ -PropertyType MultiString -Force }"
    - "else { Set-ItemProperty -Path $serviceKey -Name Environment -Value $proxyVariables\
      \ }"
    - "Restart-Service AmazonSSMAgent"
    - "Invoke-Expression \"netsh.exe winhttp set proxy $proxy `\"$no_proxy`\"\""
    - "Invoke-Expression \"bitsadmin /util /setieproxy localsystem MANUAL_PROXY $proxy\
      \ `\"$no_proxy`\"\""
    - "Restart-Computer"
  name: "ConfigureWindowsProxySettings"
  action: "aws:runPowerShellScript"
  precondition:
    StringEquals:
    - platformType
    - Windows
- inputs:
    runCommand:
    - "#!/bin/bash"
    - "set -e"
    - "PROXY=\"http://proxy.acme.aws:3128\""
    - "NOPROXY=\"169.254.169.254,ssm.eu-west-1.amazonaws.com,ec2.eu-west-1.amazonaws.com,ec2messages.eu-west-1.amazonaws.com\""
    - "mkdir -p /etc/systemd/system/snap.amazon-ssm-agent.amazon-ssm-agent.service.d"
    - "cat << EOF > /etc/systemd/system/snap.amazon-ssm-agent.amazon-ssm-agent.service.d/override.conf"
    - "[Service]"
    - "Environment=\"http_proxy=$PROXY\""
    - "Environment=\"https_proxy=$PROXY\""
    - "Environment=\"no_proxy=$NOPROXY\""
    - "EOF"
    - "systemctl daemon-reload"
    - "systemctl restart snap.amazon-ssm-agent.amazon-ssm-agent.service"
    - "cat << EOF > /etc/apt/apt.conf.d/02proxy"
    - "Acquire {"
    - "HTTP::proxy \"$PROXY\";"
    - "HTTPS::proxy \"$PROXY\";"
    - "}"
    - "EOF"
    - "echo \"Proxy configuration complete.\""
  name: "ConfigureLinuxProxySettings"
  action: "aws:runShellScript"
  precondition:
    StringEquals:
    - platformType
    - Linux
```


## task2
### SystemsManagerのドキュメント(PostMigrationAutomation)の新しいバージョンを作成する
```
schemaVersion: '0.3'
description: SSM Automation to configure proxy settings, apply patches and set tags
assumeRole: arn:aws:iam::506492377502:role/LabStack-prewarm-a1b33743-8d58-4d-SSMAutomationRole-PODAAsSw2BpU
parameters:
  InstanceId:
    description: List of Instances ID on which the automation will run.
    type: StringList
mainSteps:
  - name: tag_start
    action: aws:createTags
    nextStep: RunCommandOnInstances
    isEnd: false
    inputs:
      ResourceIds:
        - '{{InstanceId}}'
      ResourceType: EC2
      Tags:
        - Value: postmigration_started
          Key: migration_status
  - name: RunCommandOnInstances
    action: aws:runCommand
    nextStep: apply_patch
    isEnd: false
    inputs:
      DocumentName: ConfigureProxy
      InstanceIds: '{{ InstanceId }}'
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


## task3
### EventBridgeルール(PostMigrationRule)のターゲットタイプを編集
```
{
  "instanceid": "$.detail.requestParameters.resourcesSet.items[*].resourceId"
}
```
