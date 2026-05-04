## 前提条件
- VPC内にNFSサーバー(EC2)が存在する
    - /data/src配下にファイルが存在する
- 送信先S3バケットが存在する
- datasyncのVPCエンドポイント作成
    - エンドポイントセキュリティグループ
        - エージェントEC2からの443,111,1024-1064許可
    
- NFSサーバーのセキュリティグループ
    - agentのセキュリティグループからのNFS許可

### NFSサーバー設定
#### NFSサーバー起動
```
systemctl start nfs-server
```
#### /etc/exports編集
**fsid=0がついているパスが/の扱いになる**
```
/data/src {VPCのCIDR}(rw,sync,no_root_squash,fsid=0)
```

#### 設定適用
```
sudo exportfs -ra
sudo exportfs -v
```

### エージェント作成
- AMI取得コマンド
```
aws ssm get-parameter --name /aws/service/datasync/ami --region <リージョン>
```

- 取得したAMIでEC2起動
    - パブリックIP割り当てなし(Elastic IP を使用)
    - プライベートサブネット(一時的にIGWにルーティング)

- DataSync → エージェント → エージェント作成
    - ハイパーバイザー:EC2
    - エージェントのアドレス:エージェントEC2に割り当てたパブリックIP
### ロケーション作成
- 送信元
    - NFSサーバー:NFSサーバー(EC2)のプライベートIP
    - マウントパス:/

- 送信先
    - S3

