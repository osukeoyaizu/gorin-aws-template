## task1
IAMロール(lambda_execution_role)のIAMポリシー(JAMAWSLambdaPolicy)を編集し、"dynamodb:Query"を追加する
```
"Action": [
  "dynamodb:BatchGetItem",
  "dynamodb:GetItem",
  "dynamodb:PutItem",
  "dynamodb:Query"
]
```

## task2
### テーブルにデータ登録
#### レコード①
```
{
  "CustomerID": {
    "S": "Customer1"
  },
  "OrderID": {
    "N": "1"
  },
  "CommonAttribute_OrderTotal": {
    "N": "254"
  },
  "RestrictedAttribute_PII_Data": {
    "S": "No 123, street 15, India"
  }
}
```

#### レコード②
```
{
  "CustomerID": {
    "S": "Customer2"
  },
  "CommonAttribute_OrderTotal": {
    "N": "334"
  },
  "OrderID": {
    "N": "2"
  },
  "RestrictedAttribute_PII_Data": {
    "S": "No 456, street 145, NZ"
  }
}
```

## task3,4
IAMロール(lambda_execution_role)のIAMポリシー(JAMAWSLambdaPolicy)のCondition句を変更する
```
"Condition": {
    "StringEqualsIfExists": {
        "dynamodb:Select": "SPECIFIC_ATTRIBUTES"
    },
    "ForAllValues:StringEquals": {
        "dynamodb:LeadingKeys": "Customer1",
        "dynamodb:Attributes": [
            "CustomerID",
            "OrderID",
            "CommonAttribute_OrderTotal"
        ]
    }
}
```
