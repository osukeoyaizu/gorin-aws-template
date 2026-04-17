## デバイスセットアップ
https://catalog.us-east-1.prod.workshops.aws/workshops/b3e0b830-79b8-4c1d-8a4c-e10406600035/ja-JP

### Amazonlinux:2023
```
unzip connect_device_package.zip
chmod +x start.sh
```
```
rpm -qa | grep -i awscr

sudo yum remove　-y {上のコマンドで表示されたもの}
```

```
./start.sh
```

### Ubuntu
```
sudo apt update
sudo apt install -y unzip python3 python3-pip python3-full python3-venv
```

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

```
python3 -m venv venv
source venv/bin/activate
```

```
chmod +x start.sh
./start.sh
```



## 最小ポリシー
ito:Connect	arn:aws:iot:ap-northeast-1:807646278493:client/{CliendId}

ito:Publish	arn:aws:iot:ap-northeast-1:807646278493:topic/{Topic名}


