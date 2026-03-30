## Timestamp取得
{
  "timestamp.$": "$$.Execution.StartTime",
}

## uuid取得
{
	"uuid.$": "States.UUID()"
}

## Jsonに変換する
{
	"body.$": "States.StringToJson($.Body)"
}


## 数値を文字列に変換する
{
    "N.$": "States.JsonToString($num)"
}


## 文字列置き換え
{
	"MediaFileUri.$": "States.Format('s3://{}/{}',$.bucket,$.key)"
}



