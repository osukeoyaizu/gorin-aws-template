## task1
jam-challenge-patientdata-[region]-[account-id]のバケットポリシー設定
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::[account-id]:user/USER-A"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::jam-challenge-patientdata-[region]-[account-id]",
                "arn:aws:s3:::jam-challenge-patientdata-[region]-[account-id]/*"
            ]
        },
        {
            "Sid": "Statement2",
            "Effect": "Deny",
            "Principal": {
                "AWS": "arn:aws:iam::[account-id]:user/USER-B"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::jam-challenge-patientdata-[region]-[account-id]",
                "arn:aws:s3:::jam-challenge-patientdata-[region]-[account-id]/*"
            ]
        }
    ]
}
```

## task2
patientdataバケットにpatient.csvファイルをアップロードする

patientdataバケットでアクセスログの設定をし、保存先としてaccesslogsバケットを選択する
