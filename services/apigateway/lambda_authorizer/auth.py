import json

def lambda_handler(event, context):
    # 例
    parameter = event['headers']['auth']
    effect = 'Deny'
    if parameter == 'admin':
        effect = 'Allow'

    # 定形
    return {
        'principalId': '*',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': event['methodArn']
                }
            ]
        }
    }
