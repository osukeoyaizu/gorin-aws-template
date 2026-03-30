## task1

SecurityStack/LocalCloudInstanceにセッションマネージャーで接続

パラメータストアにある情報を使用してSecurityStack/OnPremiseInstanceにssh接続

パラメータストアにある情報を使用してアクティベーションに登録

```
sudo -E amazon-ssm-agent -register -code {ActivateCode} -id {ActivateId} -region {AWSRegion} -y

sudo systemctl restart amazon-ssm-agent.service
```

## task2

s3のゲートウェイエンドポイントを作成する

## task3
「AWS Private Certificate Authority」→「アクション」→「CA証明書をインストール」

「Role Anywhere」→Trust Anchorsを作成する

## task4
https://docs.aws.amazon.com/ja_jp/privateca/latest/userguide/PcaIssueCert.html
### 証明書を発行
```
sudo aws acm-pca issue-certificate \
  --certificate-authority-arn "arn:aws:acm-pca:{AWSRegion}:{AWSAccountId}:certificate-authority/{CertificateId}" \
  --csr file://csr.pem \
  --signing-algorithm "SHA256WITHRSA" \
  --validity Value=30,Type="DAYS" \
  --region {AWSRegion}
```
**出力されたARNを回答する**

### 証明書を取得
```
sudo aws acm-pca get-certificate \
  --certificate-authority-arn "arn:aws:acm-pca:{AWSRegion}:{AWSAccountId}:certificate-authority/{CertificateId}" \
  --certificate-arn "arn:aws:acm-pca:us-west-2:123456789012:certificate/my-certificate-123" \
  --region {AWSRegion} \
  --query 'Certificate' --output text > cert.pem
```

## task5
https://docs.aws.amazon.com/rolesanywhere/latest/userguide/credential-helper.html
```
sudo aws s3 cp s3://hybrid-cloud-storage-{region}-{account-id}/aws_signing_helper .
sudo chmod +x aws_signing_helper
```
```
./aws_signing_helper credential-process \
   --certificate ./cert.pem \
   --private-key ./private-key.pem \
   --trust-anchor-arn {IAM Roles Anywhere Trust Anchor ARN} \
   --profile-arn {IAM Roles Anywhere Profile ARN} \
   --role-arn arn:aws:iam::{AWSAccountId}:role/JAMIAMRolesAnywhereRole\
   --region {AWSRegion}
```

### 出力された一時的な認証情報を使用するように設定する
```
export AWS_ACCESS_KEY_ID={access_key}
export AWS_SECRET_ACCESS_KEY={secret_access_key}
export AWS_SESSION_TOKEN={session_token}
```

### シークレットの値を取得する(回答用)
```
aws secretsmanager get-secret-value --secret-id <secret-arn> --region <region>
```


## task6
### s3バケット(jam-output-bucket-{region}-{account-id})のバケットポリシーを編集する
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyPublicReadWrite",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "<bucket-arn>/*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        },
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<account>:role/JAMIAMRolesAnywhereRole"
            },
            "Action": "s3:PutObject",
            "Resource": "<bucket-arn>/*"
        }
    ]
}
```

### ファイルをアップロードする
```
aws s3 cp cert.pem s3://<バケット名>
aws s3 cp csr.pem s3://<バケット名>
```
