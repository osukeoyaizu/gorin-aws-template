import json
import boto3

ssm = boto3.client('ssm')

def send_command(document_name, EC2InstanceId):
    response = ssm.send_command(
        InstanceIds = [EC2InstanceId],
        DocumentName = document_name
        ) 
    return response


def lambda_handler(event, context):
    document_name = 'lab2-dcument'
    EC2InstanceId = event['detail']['EC2InstanceId']

    response = send_command(document_name, EC2InstanceId)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }