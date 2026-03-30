## 関数URL
### 認証タイプ(AWS_IAM)
#### リソースポリシー
```
{
  "Version": "2012-10-17",
  "Id": "default",
  "Statement": [
    {
      "Sid": "policy1",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:root"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:<region>:<account-id>:function:<function-name>",
      "Condition": {
        "Bool": {
          "lambda:InvokedViaFunctionUrl": "true"
        }
      }
    },
    {
      "Sid": "policy2",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:root"
      },
      "Action": "lambda:InvokeFunctionUrl",
      "Resource": "arn:aws:lambda:<region>:<account-id>:function:<function-name>",
      "Condition": {
        "StringEquals": {
          "lambda:FunctionUrlAuthType": "AWS_IAM"
        }
      }
    }
  ]
}
```

#### curlでアクセス
```
curl --aws-sigv4 "aws:amz:{REGION}:lambda"   --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY"   --header "X-Amz-Security-Token: $AWS_SESSION_TOKEN"   "{関数URL}"
```


### 認証タイプ(NONE)
**※コンテナを使用し、イメージを変更した場合は一度リソースポリシーを削除し、認証タイプを設定し直す必要がある。**
