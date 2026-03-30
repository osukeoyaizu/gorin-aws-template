## task1
### CodeCommitから承認ルールテンプレート(PROD_APPROVAL_TEMPLATE)を編集する
承認者のタイプ:SeniorDevelopers/*

ブランチ名:Prod

リポジトリ:WebApplicationRepo

## task2
1.Dev→Prodのプルリクエストを作成

2.SeniorDevelopersロールでサインイン

3.プルリクエストを承認

4.Prodブランチにマージする


## task3
### EventBridgeルール(ApprovalFlowEventTriggerForNewRepo)のイベントパターンを編集する
```
{
  "detail-type": ["AWS API Call via CloudTrail"],
  "source": ["aws.codecommit"],
  "detail": {
    "eventSource": ["codecommit.amazonaws.com"],
    "eventName": ["CreateRepository"]
  }
}
```

ターゲット:Lambda(ApprovalFlowLambdaFunctionForNewRepo)
