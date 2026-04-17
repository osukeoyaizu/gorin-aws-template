## インストール
```
sudo dnf update -y
sudo dnf install -y redis6
```
```
curl -O https://www.amazontrust.com/repository/AmazonRootCA1.pem
redis6-cli -c -h clustercfg.oyaizu.1fd2xb.memorydb.us-east-1.amazonaws.com   -p 6379   --tls   --cacert AmazonRootCA1.pem
```

## 操作
### 追加
set {keyの値} {valueの値}

### 取得
get {keyの値}

### 削除
del mykey