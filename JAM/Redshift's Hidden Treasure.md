## task1
**LambdaをVPC(プライベートサブネット)に配置する。セキュリティグループはdefaultでない方をアタッチする**

## task2
### IAMロール(redshift_attached_role)にインラインポリシー作成
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-jam-challenge-raw-data-{account-id}/data/*",
                "arn:aws:s3:::aws-jam-challenge-raw-data-{account-id}"
            ]
        }
    ]
}
```

## task3
### Lambda関数実行後、クエリエディタv2でSecretsManagerを使用して接続し、コマンドを実行する
```
CREATE ROLE analytics_role;

GRANT ROLE analytics_role TO analyst;

CREATE MASKING POLICY mask_phone WITH (phone VARCHAR(256)) USING ('XXXX'::TEXT);

ATTACH MASKING POLICY mask_phone ON customer_table(phone) TO ROLE analytics_role;

SET SESSION AUTHORIZATION analyst;
    
SELECT * from customer_table;
```
