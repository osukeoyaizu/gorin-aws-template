## task1,2,3
```
import os
import boto3
import json

QUEUE_URL = os.getenv("QUEUE_URL", default="test")
sqs = boto3.client('sqs')

# Function to send the message to SQS
def send_message_to_sqs(body):
    print('Sending message to SQS')
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(body)
    )

# task1
# Function to test if a string is a US zip code
def is_us_zip_code(zip_code):
    return len(zip_code) == 5 and zip_code.isdigit()

# task2
# Function to test if a string is an email using a regular expression
def is_email(email):
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# # This is a sample message body that will be sent to SQS
#      sample = {
#        "username": "john",
#        "email": "john@example.com",
#        "first_name": "John",
#        "last_name": "Doe",
#        "age": 30,
#        "city": "New York",
#        "state": "NY",
#        "zip": "10001",
#        "country": "USA"
#   }
# Function to test if required fields are present in the message body

# task3
def test_required_fields(body):
    required_fields = ['username', 'email', 'first_name', 'last_name', 'age', 'city', 'state', 'zip', 'country']
    for field in required_fields:
        if field not in body:
            return False
    return True

# Lambda function to publish Users to a queue
def lambda_handler(event, context):
    print(event)
    try:
        body = json.loads(event['body'])
        send_message_to_sqs(body)
        # task1
        if 'zip' in body and not is_us_zip_code(body['zip']):
            return {'statusCode': 400, 'body': 'Invalid zip code'}
        # task2
        if 'email' in body and not is_email(body['email']):
            return {'statusCode': 400, 'body': 'Invalid email'}
        # task3
        if not test_required_fields(body):
            return {'statusCode': 400, 'body': 'Missing required fields'}
        return {'statusCode': 200}
    except Exception as e:
        print(e)
        return {'statusCode': 500}

```


