## task1
ディストリビューション(production)のビヘイビアからHTTPS onlyに変更する

## task2
### オリジンバケットのバケットポリシー
```
{
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity <origin access identity ID>"
    },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::<bucket-name>/*"
}
```
