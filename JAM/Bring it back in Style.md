## task1
```
image.jpeg
```
## task2
```
static-assets-s3-bucket-[account-id]
```

## task3
### コンソール
static-assets-s3-bucket-[account-id]/image.jpegをパブリックアクセスにする

### AWS CLI
```
aws s3api put-object-acl --bucket <バケット名> --key image.jpeg --acl public-read
```

## task4
### コンソール
static-assets-s3-bucket-[account-id]のCORS設定
```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

### AWS CLI
#### jsonファイル作成
```
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET"],
      "AllowedOrigins": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```
#### バケットのCORS設定変更
```
aws s3api put-bucket-cors --bucket <バケット名> --cors-configuration file://cors.json
```


