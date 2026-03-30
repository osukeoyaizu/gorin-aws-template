## task1
**jam-codedeploy-<account-id>-<region>バケットにsource.zipをアップロードする**
### appspec.ymlの内容
```
# this is optional
version: 0.0
os: linux
files:
  - source: /
    destination: /opt/codedeploy/
hooks:
  ApplicationStop:
    - location: deploy/applicationstop.sh
      timeout: 60
      runas: root
  BeforeInstall:
    - location: deploy/before.sh
      timeout: 300
      runas: root
# INSTALL IS USED BY CODEDEPLOY SERVICE

  ApplicationStart:
    - location: deploy/applicationstart.sh
      timeout: 90
      runas: root

```
## task2
**CodeDeployでアプリケーション(jam-app)をコンピューティングプラットフォーム(EC2/オンプレミス)で作成する**

**デプロイグループ(jam)を作成する**

## task3
**s3のsource.zipを使用してデプロイする**

