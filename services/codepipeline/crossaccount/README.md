## クロスアカウントデプロイ
### iamロール
- codepipelineロール
```
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Principal": {
              "Service": "codepipeline.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
      }
  ]
}
```
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "codecommit:*",
                "codebuild:*",
                "sts:AssumeRole",
                "kms:*"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

- デプロイステージで使用するロール(アカウントB)
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{アカウントAのID}:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Action": [
				"s3:*",
				"lambda:*",
				"kms:*",
				"logs:*"
			],
			"Resource": [
				"*"
			]
		}
	]
}
```


```json
{
  "pipeline": {
    "name": "Lambda-CrossAccount-Pipeline",
    "roleArn": "{codepipelineロールのARN}",
    "artifactStore": {
      "type": "S3",
      "location": "codepipeline-{リージョン}-{アカウントAのID}",
      "encryptionKey": {
        "type": "KMS",
        "id": "アカウントAのKMSキーARN"
        }
    },
    "stages": [
      {
        "name": "Source",
        "actions": [
          {
            "name": "Source",
            "actionTypeId": {
              "category": "Source",
              "owner": "AWS",
              "provider": "CodeCommit",
              "version": "1"
            },
            "outputArtifacts": [
              {
                "name": "SourceArtifact"
              }
            ],
            "configuration": {
              "RepositoryName": "{リポジトリ名}",
              "BranchName": "master",
              "PollForSourceChanges": "false"
            },
            "runOrder": 1
          }
        ]
      },
      {
        "name": "Build",
        "actions": [
          {
            "name": "Build",
            "actionTypeId": {
              "category": "Build",
              "owner": "AWS",
              "provider": "CodeBuild",
              "version": "1"
            },
            "inputArtifacts": [
              {
                "name": "SourceArtifact"
              }
            ],
            "outputArtifacts": [
              {
                "name": "BuildArtifact"
              }
            ],
            "configuration": {
              "ProjectName": "{ビルドプロジェクト名}"
            },
            "runOrder": 1
          }
        ]
      },
      {
        "name": "Deploy",
        "actions": [
          {
            "name": "Deploy_Lambda_CrossAccount",
            "actionTypeId": {
              "category": "Deploy",
              "owner": "AWS",
              "provider": "Lambda",
              "version": "1"
            },
            "inputArtifacts": [
              {
                "name": "BuildArtifact"
              }
            ],
            "configuration": {
              "FunctionName": "{アカウントBのLambda関数名}"
            },
            "roleArn": "{アカウントBのIAMロールARN}",
            "runOrder": 1
          }
        ]
      }
    ],
    "version": 1
  }
}
```

### CodePipeline作成
aws codepipeline create-pipeline   --cli-input-json file://pipeline.json



### 既存のCodePipelineを使用する場合
```
aws codepipeline get-pipeline --name {パイプライン名} >pipeline.json
```
```
aws codepipeline update-pipeline --cli-input-json file://pipeline.json
```