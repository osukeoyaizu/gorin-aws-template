## セットアップ
```
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
```

```
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassInstaller
```

```     
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassInstaller/lib/Greengrass.jar --aws-region <リージョン> --thing-name <モノ名> --thing-group-name <モノのグループ名> --component-default-user ggc_user:ggc_group --provision true --setup-system-service true --deploy-dev-tools true
```

## レシピ&アーティファクト作成
※artifactsフォルダとrecipesフォルダ作成

### ローカルデプロイ
**コンポーネント名=com.aws.TempThresholdAnomaly, バージョン=1.0.6**

エラーのあるデプロイメントを削除した後、最後のデプロイメントを作成
```
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.aws.TempThresholdAnomaly"
```

デプロイ
```
sudo /greengrass/v2/bin/greengrass-cli deployment create \
    --recipeDir ~/environment/Greengrass/recipes \
    --artifactDir ~/environment/Greengrass/artifacts \
    --merge "com.aws.TempThresholdAnomaly=1.0.6"
```


### カスタムコンポーネント公開
アーティファクトをS3バケットにアップロード
```
aws s3 cp --recursive ~/environment/AWSIoTGreenGrass/ s3://$S3_BUCKET/
```

コンポーネント定義作成
```
cd ~/environment/AWSIoTGreenGrass/recipes
aws greengrassv2 create-component-version  --inline-recipe fileb://<レシピファイル> --region <リージョン>
```

「マネジメントコンソール」→「AWS IoT」→「Greengrass」→「デプロイ」からバージョンを指定してデプロイ


### エラー確認コマンド
```
sudo tail -F /greengrass/v2/logs/greengrass.log
sudo tail -f /greengrass/v2/logs/com.aws.TempThresholdAnomaly.log
```
