## task1
KMSのカスタマーマネージドキーの削除をキャンセル、有効化し、キーポリシーのDenyをAllowに変更する

s3からKeyToGetPasswordファイルをダウンロードする
```
aws kms decrypt ^
    --ciphertext-blob fileb://KeyToGetPassword ^
    --key-id <key-id> ^
    --output text ^
    --query Plaintext > Output.base64 --region <region>
```
**Output.base64ファイルの内容をbase64デコードしてOutput.txtファイルに保存する**

## task2

### Windowsの場合
```
certutil -decodehex Output.txt output.bin
```

### Linuxの場合
```
xxd -r -p Output.txt output.bin
```

###  SSE-C パラメータを指定した s3 cp コマンドを使用して、パスワードファイルをダウンロード
```
aws s3 cp s3://<bucket-name>/Password.txt password_retrived.txt --sse-c AES256 --sse-c-key fileb://output.bin 
```

