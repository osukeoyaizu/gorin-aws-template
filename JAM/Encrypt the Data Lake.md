## デフォルトの暗号化選定
```
aws s3api put-bucket-encryption ^
  --bucket <BUCKET-NAME> ^
  --server-side-encryption-configuration "{\"Rules\":[{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\":\"aws:kms\",\"KMSMasterKeyID\":\"<KMS-KEY-ARN>\"}}]}"
```

## ETag取得
```
aws s3api head-object --bucket <BUCKET-NAME> --key reports/manifest.csv
```

## デフォルトの暗号化選定
```
aws s3control create-job ^
  --account-id {ACCOUNT-ID} ^
  --operation "{\"S3PutObjectCopy\":{\"TargetResource\":\"arn:aws:s3:::encrypt-data-lake-{ACCOUNT-ID}\",\"SSEAwsKmsKeyId\":\"{KMSのキーID}\",\"MetadataDirective\":\"REPLACE\",\"NewObjectMetadata\":{\"SSEAlgorithm\":\"KMS\"}}}" ^
  --report "{\"Enabled\":false}" ^
  --manifest "{\"Spec\":{\"Format\":\"S3BatchOperations_CSV_20180820\",\"Fields\":[\"Bucket\",\"Key\"]},\"Location\":{\"ObjectArn\":\"arn:aws:s3:::encrypt-data-lake-{ACCOUNT-ID}/reports/manifest.csv\",\"ETag\":\"\\\"{ETagの値}\\\"\"}}" ^
  --description "Re-encrypt using KMS" ^
  --priority 10 ^
  --role-arn arn:aws:iam::{ACCOUNT-ID}:role/FixEncryptionRole ^
  --region {region}
```

