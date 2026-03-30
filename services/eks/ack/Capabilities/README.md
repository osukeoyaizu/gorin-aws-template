## 機能を有効化する
### マニフェストサンプルサイト
https://aws-controllers-k8s.github.io/community/docs/community/services/


#### S3バケット
https://github.com/aws-controllers-k8s/s3-controller/blob/main/test/e2e/resources/bucket.yaml

### 権限
- 機能ロールに必要な権限をアタッチする
- アクセスエントリで機能ロールに「AmazonEKSClusterAdminPolicy」を追加する
