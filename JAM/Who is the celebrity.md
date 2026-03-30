## task1
### s3のイベント通知を作成する
名前:任意

イベントタイプ:All

フィルター:Images/

送信先:Lambda(as-if-photo-studio-RecognizeFaces)


## task2
### Lambda(as-if-photo-studio-RecognizeFaces)の環境変数設定
キー:TABLE_NAME

値:as-if.photo.studio.db

## task3
Lambdaのロールのポリシーにステートメント追加
```
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:ap-northeast-1:{account-id}:table/as-if.photo.studio.db"
            ]
        }
```


## task4
### Lambda(as-if-photo-studio-RecognizeFaces)のコードを編集(40~45行目)
```
    response = table.put_item(
        Item={
            'Key': key,
            'names': names,
        }
    )
```
