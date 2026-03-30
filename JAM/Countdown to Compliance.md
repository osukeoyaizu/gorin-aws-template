## task1
ec2インスタンスのセキュリティグループのルールを編集する

インバウンド:MyIPからのRDPを許可する

アウトバウンド:送信先を0.0.0.0に変更する

## task2
### RDP接続したWindowsのPowerShellで実行する
```
Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "WUServer"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "WUStatusServer"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "UseWUServer"
```
**EC2インスタンスを再起動してRDP接続する**

**ステートマネージャー(Production-Patching)の関連付けを今すぐ適用する**


## task3
### ステートマネージャー(Production-Configuration)を編集する

パラメータのCommandsの「exit 1」を「exit 0」に変更して保存する

```
# OS CONFIGURATION CHANGES DEPLOYING.......
Write-Host "Please remove below exit code line or change it to exit 0 instead."
exit 0
```

