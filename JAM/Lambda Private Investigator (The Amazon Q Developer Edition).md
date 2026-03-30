## task1
Lambda関数(lambda-pi)編集
```
import os
import boto3

s3 = boto3.client("s3")
def lambda_handler(event, context):
    # Get secret content
    secret_content = (
        s3.get_object(Bucket=os.getenv("S3_BUCKET"), Key=os.getenv("S3_OBJECT_KEY"))[
            "Body"
        ]
        .read()
        .decode("utf-8")
    )
    return {"statusCode": 200, "body": secret_content}
```
