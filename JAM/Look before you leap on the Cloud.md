## task1
Lambda関数(MyFunction)のサブネットをプライベートサブネットにする

## task2
IAMロール(出力プロパティのJamTask2IAMRole)のIAｍポリシー(CustomPolicyForS3Access)のGwt,Put,Deleteのリソースに「/*」をつける

## task3
IAMロール(jam-aws-tmp-admin-role)に切り替える

### キーポリシーのプリンシパルを追加する
```
      "Principal": {
        "AWS": [
          "arn:aws:iam::{account-id}:role/jam-aws-tmp-admin-role",
          "<出力プロパティのJamTask3SecurityAdminRoleArn>"
        ]
      },
```

## task4
### バケットポリシーのプリンシパルを編集する
```
"Principal": {
"AWS": "arn:aws:iam::739275461757:role/S3CrossAccountAccess"
},
```
