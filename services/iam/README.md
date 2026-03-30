## タグ
### 特定のタグがついているEC2インスタンスの停止を拒否
キー:Department,値:Marketing
```
  {
    "Action": "ec2:StopInstances",
    "Effect": "Deny",
    "Resource": "*",
    "Condition": {
      "StringEqualsIgnoreCase": {
        "aws:ResourceTag/Department": "Marketing"
     }
    }
   }
```

### ユーザーのタグ (aws:PrincipalTag/Project) とリソースのタグ (aws:ResourceTag/Project) が一致する場合にのみ許可
```
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Project": "${aws:PrincipalTag/Project}"
        }
      }
```

### 作成リクエストに「Project」タグが含まれている
```
    {
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*",
        "arn:aws:ec2:*:*:volume/*"
      ],
      "Condition": {
        "ForAllValues:StringEquals": {
          "aws:TagKeys": [
            "Project"
          ]
        }
      }
    }
```

### RunInstances アクションに伴うタグ付けのみ許可
```
"Action": ["ec2:CreateTags"],
"Resource": [
  "arn:aws:ec2:*:*:instance/*",
  "arn:aws:ec2:*:*:volume/*"
],
"Condition": {
  "StringEquals": {
    "ec2:CreateAction": ["RunInstances"]
  }
}
```

## 権限境界
### 管理者にアタッチするポリシー
※ユーザー作成時に境界ポリシーを設定しなければ拒否される
```
{
    "Sid": "CreateOrChangeOnlyWithBoundary",
    "Effect": "Allow",
    "Action": [
        "iam:AttachUserPolicy",
        "iam:CreateUser",
        "iam:DeleteUserPolicy",
        "iam:DetachUserPolicy",
        "iam:PutUserPermissionsBoundary",
        "iam:PutUserPolicy"
    ],
    "Resource": "*",
    "Condition": {
        "StringEquals": {
            "iam:PermissionsBoundary": "arn:aws:iam::{account-id}:policy/{境界ポリシー}"
        }
    }
}
```

## VPC内 or AWSサービスからの操作のみを許可する
- aws:ec2InstanceSourceVPC が指定VPCと一致しない（true）

- aws:ViaAWSService が false（true）

→両方がtrueだとDeny
```
{
    "Version": "2012-10-17",
    "Statement": [{
    	"Effect": "Deny",
    	"Action": "*",
        "Resource": "*",
    	"Condition": {
  	      "StringNotEquals": {
        	    "aws:ec2InstanceSourceVPC": "${aws:SourceVpc}"
    	    },
 	       "BoolIfExists": {
            	"aws:ViaAWSService": "false"
        	}
    	}
	}]
}
```

## Roles Anywhereを使用してオンプレサーバーに権限を与える
https://dev.classmethod.jp/articles/iam-roles-anywhere-with-aws-pca/
### Private CA作成
「AWS Private Certificate Authority」→「認証機関を作成」

組織名などを適当に入力する

キーアルゴリズム:RSA 2048

### 信頼アンカーを作成
認証機関:AWS証明管理プライベートCA

※作成済のプライベートCAを指定する

### クライアントが引き受けるIAMロールを作成
#### 信頼ポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "rolesanywhere.amazonaws.com"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:SetSourceIdentity",
                "sts:TagSession"
            ]
        }
    ]
}
```

### プロファイル作成
作成したIAMロールを指定する

### クライアント側での操作
#### 証明書の署名リクエストファイル(csr.pem)と秘密鍵(private-key.pem)を作成
```
openssl req -out csr.pem \
-new -newkey rsa:2048 -nodes \
-keyout private-key.pem
```

#### クライアント証明書発行
https://docs.aws.amazon.com/ja_jp/privateca/latest/userguide/PcaIssueCert.html
```
aws acm-pca issue-certificate   --certificate-authority-arn {プライベートCAのARN}   --csr fileb://csr.pem   --signing-algorithm SHA256WITHRSA  --validity Value=7,Type=DAYS
```

#### jqコマンドインストール
```
sudo dnf install jq
```

#### 証明書取得
```
aws acm-pca get-certificate   --certificate-authority-arn {プライベートCAのARN}   --certificate-arn  {証明書のARN}|  jq -r  .'Certificate' > cert.pem
```

#### 一時クレデンシャルを要求するヘルパーツールを取得
https://docs.aws.amazon.com/ja_jp/rolesanywhere/latest/userguide/credential-helper.html
```
wget https://rolesanywhere.amazonaws.com/releases/1.7.1/X86_64/Linux/Amzn2023/aws_signing_helper
chmod 755 aws_signing_helper
```

#### 一時クレデンシャル取得
```
./aws_signing_helper credential-process   --certificate ./cert.pem   --private-key ./private-key.pem   --trust-anchor-arn {信頼アンカーARN}   --profile-arn {プロファイルARN}  --role-arn {IAMロールARN} | jq .
```

#### 認証情報を設定
```
export AWS_ACCESS_KEY_ID={access_key}
export AWS_SECRET_ACCESS_KEY={secret_access_key}
export AWS_SESSION_TOKEN={session_token}
```
→IAMロールの権限でAWSリソースにアクセス可能

