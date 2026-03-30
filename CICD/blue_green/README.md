## service-bluegreen.json
https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/create-blue-green.html
```
{
    "cluster": "<クラスター名>",
    "serviceName": "<サービス名>",
    "taskDefinition": "<タスク定義名>",
    "loadBalancers": [
        {
            "targetGroupArn": "<ターゲットグループのarn>",
            "containerName": "<コンテナ名>",
            "containerPort": <コンテナポート>
        },
        {
            "targetGroupArn": "<ターゲットグループのarn>",
            "containerName": "<コンテナ名>",
            "containerPort": <コンテナポート>
        }
    ],
    "launchType": "FARGATE",
    "schedulingStrategy": "REPLICA",
    "deploymentController": {
        "type": "CODE_DEPLOY"
    },
    "platformVersion": "LATEST",
    "networkConfiguration": {
       "awsvpcConfiguration": {
          "assignPublicIp": "DISABLED",
          "securityGroups": [ "<セキュリティグループID>" ],
          "subnets": [ "<サブネットID-1>", "<サブネットID-2>" ]
       }
    },
    "desiredCount": 2,
    "tags": [{"key":"Owner","value":"oyaizu"}]
}
```
## サービス作成コマンド(CLI)
```
aws ecs create-service \
     --cli-input-json file://service-bluegreen.json \
     --region <リージョンコード>
```

## CodeDeployに必要な権限
AWSCodeDeployRole

AWSCodeDeployRoleForECS

## CodeBuildに必要な権限
AmazonEC2ContainerRegistryPowerUser

kms(リポジトリが暗号化されている場合)

## CodePipelineに必要な権限
ecs:TagResource(タスク定義にタグ付けされている場合)

kms(リポジトリが暗号化されている場合)
