## ルール
### 特権モードにチェックがついているビルドプロジェクトを検出
codebuild-project-environment-privileged-check

### CodeBuildプロジェクトの環境変数にAWS認証情報がハードコードされていないかをチェック
codebuild-project-envvar-awscred-check


## カスタムルール
### セキュリティグループの全許可を検出
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


## 修復アクション

### すべての送信元アドレスからのトラフィックを許可する、指定したセキュリティグループからすべての進入ルールを削除
https://docs.aws.amazon.com/ja_jp/systems-manager-automation-runbooks/latest/userguide/automation-aws-remove-unrestricted-source-ingress.html
```
AWSConfigRemediation-RemoveUnrestrictedSourceIngressRules
```
必要なアクセス許可・・・ドキュメントを参照
