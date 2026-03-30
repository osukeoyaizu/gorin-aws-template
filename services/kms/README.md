## カスタマーマネージドキーで暗号化されたファイルを復号化
```
aws kms decrypt \
    --ciphertext-blob fileb://KeyToGetPassword \
    --key-id <key-id> \
    --output text \
    --query Plaintext \
    --region <region> \
    > Output.base64

```

## SSE-Cで暗号化されたファイルを復号化
```
aws s3 cp s3://<bucket-name>/Password.txt password_retrived.txt --sse-c AES256 --sse-c-key fileb://output.bin 
```
