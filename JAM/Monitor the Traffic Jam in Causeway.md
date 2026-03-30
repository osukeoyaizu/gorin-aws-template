## task1
EC2インスタンスのセキュリティグループのアウトバウンドルールで0.0.0.0/0を許可する

## task2
```
SS9999
```

## task3
### 証明書生成
```
openssl genrsa 2048 > my-private-key.pem
openssl req -new -x509 -nodes -sha256 -days 365 -key my-private-key.pem -outform PEM -out my-certificate.pem
```

Certificate Managerの「証明書をインポート」をしてARNを回答する


## task4
```
lightning
```
