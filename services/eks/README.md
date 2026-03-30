## kubectl と eksctl のセットアップ

### kubectlをインストールまたは更新する
https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/install-kubectl.html
```
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.33.3/2025-08-03/bin/linux/amd64/kubectl
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.33.3/2025-08-03/bin/linux/amd64/kubectl.sha256
sha256sum -c kubectl.sha256
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
```

### eksctlをインストールする
https://eksctl.io/installation/
```
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check
tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz
sudo mv /tmp/eksctl /usr/local/bin
```

## クラスターの作成
### fargate,既存のVPCに作成
```
eksctl create cluster --name <クラスター名> --region <リージョンコード> --vpc-private-subnets <サブネット1>,<サブネット2> --fargate
```

### ec2,既存のVPCに作成
```
eksctl create cluster --name <クラスター名> --region <リージョンコード> --vpc-private-subnets <サブネット1>,<サブネット2> --without-nodegroup
```

## 操作するクラスターの変更
```
aws eks update-kubeconfig --region {region} --name {cluster-name}
```
