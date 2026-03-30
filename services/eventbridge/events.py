import boto3
import os
import json

events = boto3.client("events")

EVENT_BUS_ARN = os.environ["EVENT_BUS_ARM"]

def put_events(source, detail_type, event):
    events.put_events(
        Entries=[
            {
                "Source": source,
                "DetailType": detail_type,
                "Detail": json.dumps(event),
                "EventBusName": EVENT_BUS_ARN,
            }
        ]
    )

def handler(event, context):
    source = "Publisher Lambda"
    detail_type = "In coming order"

    put_events(source, detail_type, event)
