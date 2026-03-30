## task1
Elastic IP(EppEIP)をTask1インスタンスに関連付ける

### Task1インスタンスに接続してs3からファイルをダウンロードする
```
sudo aws s3 cp s3://task1-challenge-bucket-xxxxxxxx/answer.txt ./ --region <region-name>
cat answer.txt; echo
```

## task2
Task2のIAMロールをApp_Roleに変更する

### Task1インスタンスに接続してs3からファイルをダウンロードする
```
sudo aws s3 cp s3://task2-challenge-bucket-xxxxxxxx/answer.txt ./ --region <region-name>
cat answer.txt; echo
```

## task3
セキュリティグループ(AppSG)をTask3インスタンスに関連付ける
```
sudo aws s3 cp s3://task3-challenge-bucket-xxxxxxxx/answer.txt ./ --endpoint-url https://bucket.<s3インターフェースエンドポイント固有の値>.s3.<リージョン>.vpce.amazonaws.com --region <region-name>
cat answer.txt; echo
```
