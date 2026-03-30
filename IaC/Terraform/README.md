## 使い方
### インストール
```
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform
```

### 初回実行
```
terraform init
```

### 定義内容のチェック
```
terraform plan
```

### 定義を適用
```
terraform apply
```

### 削除
```
terraform destroy
```
