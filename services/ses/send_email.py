import os
import json
import boto3

ses = boto3.client("ses", region_name="us-east-1")

FROM_EMAIL = os.environ["FROM_EMAIL"]

def send_email(to_address, subject, body):
    response = ses.send_email(
            Source=FROM_EMAIL,
            Destination={"ToAddresses": [to_address]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Text": {"Data": body, "Charset": "UTF-8"}
                }
            }
        )
    return {
        "status": "success",
        "message_id": response["MessageId"]
    }


def lambda_handler(event, context):
    """
    event 例:
    {
        "to": "osuke_oyaizu@mail.toyota.co.jp",
        "subject": "テストメール",
        "body": "本文です"
    }
    """

    to_address = event.get("to")
    subject = event.get("subject", "No Subject")
    body = event.get("body", "test")

    result = send_email(to_address, subject, body)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
