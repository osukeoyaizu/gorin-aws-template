## Refactor Space
### 環境とアプリケーションの作成
環境名を指定して作成

アプリケーション名を指定

プロキシVPCでプライベートリンクなどで使用するVPCを指定

**API GatewayとNLBが作成される**

### サービス、ルートを作成
#### Lambdaの場合
Lambda関数とソースパスを指定する

**追加したルートに応じて自動的にAPI Gatewayでリソースパスが追加される**

#### VPCの場合
VPCとエンドを指定

**自動作成されたNLBから通信できる必要がある**

#### アクセス方法
アプリケーションのURLにルートのソースパスを指定してアクセスする


## Discovery Agent をインストール
https://docs.aws.amazon.com/ja_jp/application-discovery/latest/userguide/install.html
### Linux
```
curl -o ./aws-discovery-agent.tar.gz https://s3.{region}.amazonaws.com/aws-discovery-agent.{region}/linux/latest/aws-discovery-agent.tar.gz
tar -xzf aws-discovery-agent.tar.gz
sudo bash install -r your-home-region -k aws-access-key-id -s aws-secret-access-key
```

### Windows
AWSドキュメントからAWSDiscoveryAgentUpdater.exeをダウンロードする
```
.\AWSDiscoveryAgentInstaller.exe REGION="your-home-region" KEY_ID="aws-access-key-id" KEY_SECRET="aws-secret-access-key" /quiet
```
