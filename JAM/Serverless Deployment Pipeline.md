## task3
### AWS CLIでCodePipelineの設定をjsonファイルで取得する
```
aws codepipeline get-pipeline --name <pipeline name> --query pipeline > current.json
```

### jsonファイルのブランチをmainに変更
```
aws codepipeline update-pipeline --pipeline file://current.json
```

## task4
### index.jsファイルのreturnの値を変更してコミットする
```
  const response = {
    statusCode: 200,
    body: JSON.stringify('Hello from Lambda!'),
  };
  return response;
```

