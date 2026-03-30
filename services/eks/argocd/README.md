## 参考サイト
https://argo-cd.readthedocs.io/en/stable/getting_started/

https://qiita.com/nao-590/items/1057c63d0fa4e9c203f1

## 設定手順
### インストールする
```
kubectl create namespace argocd
```
```
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### brewコマンドをインストール
- CloudShell
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
export PATH=/home/linuxbrew/.linuxbrew/bin:$PATH
```
- EC2
```
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

```

### Argo CD CLIインストール
```
brew install argocd
```

### ロードバランサー
```
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

### ログイン
※作成されたロードバランサーにアクセスする

ユーザー名:admin

パスワード:
```
argocd admin initial-password -n argocd
```


