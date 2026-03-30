## EMR Serverless StartJobRun
API パラメータ
```
{
  "ApplicationId": "<EMR Studio ApplicationのID>",
  "ExecutionRoleArn": "arn:aws:iam::<アカウントID>:role/service-role/AmazonEMR-ExecutionRole-xxxxx",
  "JobDriver": {
    "SparkSubmit": {
      "EntryPoint": "<pythonファイルなどのS3パス>",
      "EntryPointArguments": [
        "--data_source",
        "<データソースのS3パス>",
        "--output_uri",
        "データ出力S3パス"
      ],
      "SparkSubmitParameters": "--conf spark.executor.cores=2 --conf spark.executor.memory=4g --conf spark.driver.memory=2g"
    }
  }
}
```


## エラー処理
### Lambdaがカスタムエラーを返す
```
import json
import random

class PaymentServiceUnavailable(Exception):
    pass

class PaymentDeclined(Exception):
    pass

def handler(event, context):
    order_id = event.get('orderId', 'unknown')
    # Simulate transient 503 errors (~40% of the time)
    roll = random.random()
    if roll < 0.40:
        raise PaymentServiceUnavailable('Payment gateway returned 503')
    if roll < 0.50:
        raise PaymentDeclined('Card declined by issuer')
    return {
        'orderId': order_id,
        'paymentProcessed': True,
        'transactionId': f'TXN-{order_id}-001'
    }
```


### ステートマシン
- PaymentServiceUnavailableは3回リトライ
- PaymentDeclinedはエラーキャッチする
```
{
  "Comment": "Order Processing Workflow - PaymentDeclined ends execution",
  "StartAt": "ProcessPayment",
  "States": {
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:eu-west-1:679403209867:function:process-payment-function",
      "Retry": [
        {
          "ErrorEquals": [
            "PaymentServiceUnavailable"
          ],
          "BackoffRate": 2,
          "IntervalSeconds": 2,
          "MaxAttempts": 3
        }
      ],
      "Catch": [
        {
          "ErrorEquals": [
            "PaymentDeclined"
          ],
          "Next": "EndPaymentDeclined"
        }
      ],
      "Next": "成功"
    },
    "成功": {
      "Type": "Succeed"
    },
    "EndPaymentDeclined": {
      "Type": "Succeed",
      "Comment": "Payment was declined, ending execution"
    }
  }
}
```