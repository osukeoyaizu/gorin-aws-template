## プライベート証明書を使用し、nginxをhttps
### プライベート証明機関を作成
- 組織名などを入力
- CA証明書をインストールする

### プライベート証明書を作成
- 証明機関:作成したプライベートCA
- ドメイン名:{ドメイン名}

### nginxサーバー設定
```
mkdir -p ~/acm-export && cd ~/acm-export

openssl rand -base64 48 | tr -d '\n' > passphrase.txt

aws acm export-certificate \
  --region us-east-1 \
  --certificate-arn {プライベート証明書ARN} \
  --passphrase fileb://passphrase.txt \
  --output json > export.json

jq -r '.Certificate'      export.json > cert.pem
jq -r '.CertificateChain' export.json > cert_chain.pem
jq -r '.PrivateKey'       export.json > private_key_encrypted.pem
```

```
openssl pkcs8 \
  -in private_key_encrypted.pem \
  -out private_key.pem \
  -passin file:passphrase.txt
```

```
chmod 600 private_key.pem


sudo mkdir -p /etc/nginx/ssl/{ドメイン名}
sudo mv cert.pem cert_chain.pem private_key.pem /etc/nginx/ssl/{ドメイン名}/
sudo chown -R root:root /etc/nginx/ssl/{ドメイン名}
sudo chmod 600 /etc/nginx/ssl/{ドメイン名}/private_key.pem
```

```
sudo tee /etc/nginx/conf.d/{ドメイン名}.conf > /dev/null <<'EOF'
server {
    listen 443 ssl;
    server_name {ドメイン名};

    ssl_certificate     /etc/nginx/ssl/{ドメイン名}/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/{ドメイン名}/private_key.pem;
    ssl_trusted_certificate /etc/nginx/ssl/{ドメイン名}/cert_chain.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF
```

```
sudo nginx -t
sudo systemctl restart nginx
```

#### 確認
```
curl -vk   --resolve {ドメイン名}:443:{自分のプライベートIP}   https://{ドメイン名}/
```


### Route53設定
- プライベートホストゾーン作成
    - Aレコード:nginxサーバーのプライベートIP


### クライアント側設定
#### プライベートCAからルート証明書をコピーし、root-ca.pemに貼り付ける
```
vi root-ca.pem
```

```
sudo cp root-ca.pem /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

```
curl https://{ドメイン名}
```