## task1
```
dbb
```

## task2
```
dca
```

## task3,4
ファイルをCodeCommitリポジトリにアップロードする

CodePipelineでソースステージのブランチを設定して変更をリリースする
## index.js
```
exports.handler = async function (event, context) {
    return {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),   
    }
};
```
## buildspec.yml
```
version: 0.2
 
phases:
  install:
    runtime-versions:
        nodejs: 14
    commands:
        - echo Here is where I would be installing dependencies... 
  build:
    commands:
        - echo Build started on `date`
        - zip -r9 ./deployment_package.zip .
        - echo Zipped up lambda package... 
  post_build:
    commands:
      - echo "Updating lambda Function..."
      - aws lambda update-function-code --function-name NewServerlessApplicationFunction --zip-file fileb://deployment_package.zip
      - echo "Serverless Functionality Deployed!"
```
