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

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "DoNotConnectToWindowsUpdateInternetLocations"

Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate" -Name "SetDisableUXWUAccess"
```
**EC2インスタンスを再起動してRDP接続する**

## task3
SystemsManager → パッチマネージャー → 概要から開始 → 今すぐパッチ適用 → デフォルト設定で適用する

パッチポリシーに基づかない繰り返しタスク → Patching task name → Association ID を回答する
