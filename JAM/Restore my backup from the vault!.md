## task1
ボールトから復元する

暗号化キー:DynamoDB_kms_key (アクセス権がない場合はaws/dynamodb)

IAMロール:Backup_Application_role

## task2
```
{
  "TableName": "{table-name}",
  "EmployeeId": "3853",
  "Employee Favorite sport": "Football",
  "Employee Favorite movie": "Money Train"
}
```

## task3
### バックアッププラン作成
プラン名:任意

ルール名:任意

バックアップボールト:Jam_backup_vault

バックアップ頻度:cron(0 5,22 ? * 2-6 *)

次の時間以内に開始:1時間

次の時間以内に完了:4時間

### リソース割り当て

ロール:Backup_Application_role

リソース:task1で復元したDynamoDBテーブル


