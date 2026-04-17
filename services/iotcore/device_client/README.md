## 前提条件
- Ubuntu
- ボリュームサイズ:30Gib

## Device Client セットアップ
```
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y autoremove
sudo apt-get -y install build-essential libssl-dev cmake unzip git python3-pip
```

```
export PATH=$PATH:~/.local/bin # configures the path to include the directory with the AWS CLI
git clone https://github.com/aws/aws-cli.git # download the AWS CLI code from GitHub
cd aws-cli && git checkout v2 # go to the directory with the repo and checkout version 2
pip3 install -r requirements.txt # install the prerequisite software
```

```
pip3 install . # install the AWS CLI 
```

```
mkdir ~/certs
curl -o ~/certs/AmazonRootCA1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
chmod 745 ~
chmod 700 ~/certs
chmod 644 ~/certs/AmazonRootCA1.pem
```

```
cd ~
git clone https://github.com/awslabs/aws-iot-device-client aws-iot-device-client
mkdir ~/aws-iot-device-client/build && cd ~/aws-iot-device-client/build
cmake ../
```

```
cmake --build . --target aws-iot-device-client
```

## 実行
### 設定ファイル(~/dc-configs/dc-testconn-config.json)
```
{
  "endpoint": "{エンドポイント}",
  "cert": "~/certs/{モノ名}.cert.pem",
  "key": "~/certs/{モノ名}.private.key",
  "root-ca": "~/certs/AmazonRootCA1.pem",
  "thing-name": "{モノ名}",
  "logging": {
    "enable-sdk-logging": true,
    "level": "DEBUG",
    "type": "STDOUT",
    "file": ""
  },
  "jobs": {
    "enabled": false,
    "handler-directory": ""
  },
  "tunneling": {
    "enabled": false
  },
  "device-defender": {
    "enabled": true,
    "interval": 60
  },
  "fleet-provisioning": {
    "enabled": false,
    "template-name": "",
    "template-parameters": "",
    "csr-file": "",
    "device-key": ""
  },
  "samples": {
    "pub-sub": {
      "enabled": true,
      "publish-topic": "test/dc/pubtopic",
      "publish-file": "~/.aws-iot-device-client/pubsub/publish-file.txt",
      "subscribe-topic": "test/dc/subtopic",
      "subscribe-file": "~/.aws-iot-device-client/pubsub/subscribe-file.txt"
    }
  },
  "config-shadow": {
    "enabled": false
  },
  "sample-shadow": {
    "enabled": false,
    "shadow-name": "",
    "shadow-input-file": "",
    "shadow-output-file": ""
  }
}
```

### 実行コマンド
```
cd ~/aws-iot-device-client/build
./aws-iot-device-client --config-file ~/dc-configs/dc-testconn-config.json
```



## 確実方法
### セキュリティプロファイルを作成する必要がある
- 「IoT」→「セキュリティ」→「検出」→「セキュリティプロファイル」→「セキュリティプロファイルを作成」→「ルールに基づいた異常検出プロファイルを作成」
    - 検出したいメトリクスを選択する

※注意: 前回との差分なので変更がないとメトリクスが0になってしまう