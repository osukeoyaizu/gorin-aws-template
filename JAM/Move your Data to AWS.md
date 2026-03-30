## task3
```
aws datasync create-location-s3 ^
    --s3-bucket-arn "arn:aws:s3:::<バケット名>" ^
    --subdirectory "/migrated" ^
    --s3-storage-class "STANDARD" ^
    --s3-config "BucketAccessRoleArn=<ロールARN>" ^
    --region <リージョン>
```


