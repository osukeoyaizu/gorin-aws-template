## task1
::/0,0.0.0.0/0

## task2
Config→ルールを追加→Guardを使用してカスタムルールを作成
### ルールの内容
```
rule prevent_inbound_Ipv4_access_to_any_ip when this.configuration.ipPermissions[*].ipv4Ranges !empty {  
    this.configuration.ipPermissions[*].ipv4Ranges[*].cidrIp != "0.0.0.0/0" <<  
        IPv4 Source address cannot be 0.0.0.0/0  
    >>  
}  
  
rule prevent_inbound_Ipv6_access_to_any_ip when this.configuration.ipPermissions[*].ipv6Ranges !empty {  
    this.configuration.ipPermissions[*].ipv6Ranges[*].cidrIpv6 != "::/0" <<  
        IPv6 Source address cannot be ::/0  
    >>  
}
```
**再評価をクリックする**

## task3
非準拠のセキュリティグループのルールを手動で削除

再評価する

## task4
### 修復の管理
修復方法:自動修復

修復アクションを選択:AWSConfigRemediation-RemoveUnrestrictedSourceIngressRules

AutomationAssumeRole:arn:aws:iam::{account-id}:role/SystemsManager_AutomationAssumeRole
