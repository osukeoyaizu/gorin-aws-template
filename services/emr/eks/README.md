## 前提条件
- EKSクラスター作成
    - OIDC設定済
- S3作成済
    - /input : csvなどのデータふぁいう
    - /output : ジョブの結果出力先
    - /logs : ジョブのログ出力先
    - /code : ジョブのpythonファイルなどを配置

## ジョブ実行ロール作成
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "elasticmapreduce.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
```
aws iam create-role --role-name EMRContainers-JobExecutionRole --assume-role-policy-document file://emr-trust-policy.json
```
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "logs:*",
                "kms:*"
            ],
            "Resource": "*"
        }
    ]
}
```
```
 aws iam put-role-policy --role-name EMRContainers-JobExecutionRole --policy-name EMR-Containers-Job-Execution --policy-document file://EMRContainers-JobExecutionRole.json
```


## ジョブ実行ロールの信頼ポリシーを更新
```
aws emr-containers update-role-trust-policy \
       --cluster-name {EKSクラスター名} \
       --namespace {名前空間} \
       --role-name EMRContainers-JobExecutionRole
```

## アクセスエントリ設定
- ジョブ実行ロールを追加する

## 仮想クラスターを作成
```
aws emr-containers create-virtual-cluster \
--name emr_virtual_cluster \
--container-provider '{
    "id": "{クラスター名}",
    "type": "EKS",
    "info": {
        "eksInfo": {
            "namespace": "{名前空間}"
        }
    }
}'
```



## start-job-run-request.json
```
{
  "name": "{ジョブ名}", 
  "virtualClusterId": "{仮想クラスターID}",  
  "executionRoleArn": "arn:aws:iam::{アカウントID}:role/EMRContainers-JobExecutionRole", 
  "releaseLabel": "emr-6.2.0-latest", 
  "jobDriver": {
    "sparkSubmitJobDriver": {
      "entryPoint": "{pythonファイルなどが配置してあるS3パス}",
      "entryPointArguments": ["--data_source", "{データソースのS3パス}", "--output_uri", "{データ出力S3パス}"],  
       "sparkSubmitParameters": "--conf spark.executor.instances=1 --conf spark.executor.memory=1G --conf spark.executor.cores=1 --conf spark.driver.cores=1"
    }
  }, 
  "configurationOverrides": {
    "applicationConfiguration": [
      {
        "classification": "spark-defaults", 
        "properties": {
          "spark.driver.memory":"2G"
         }
      }
    ], 
    "monitoringConfiguration": {
      "persistentAppUI": "ENABLED", 
      "cloudWatchMonitoringConfiguration": {
        "logGroupName": "{ロググループ名}", 
        "logStreamNamePrefix": "{プレフィックス}"
      }, 
      "s3MonitoringConfiguration": {
        "logUri": "{ログ出力S3パス}"
      }
    }
  }
}


```

## ジョブ実行
```
aws emr-containers start-job-run --cli-input-json file://./start-job-run-request.json
```


## ジョブステータス確認コマンド
```
aws emr-containers describe-job-run --id  {ジョブID}  --virtual-cluster-id {仮想クラスタID}
```

## アプリのログ確認コマンド
```
kubectl logs -n emr {spark-xxxxx-driver} -c spark-kubernetes-driver
```

## トラブルシューティング
- AssumeRoleWithWebIdentity:start-job-run-request.jsonで指定したロールの信頼ポリシーを確認する
- ポッドが立ち上がらない:インスタンスタイプが小さい(m5.xlarge以上)
