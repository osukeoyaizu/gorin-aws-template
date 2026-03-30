import json
import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

iam_resource = boto3.resource('iam')
accessanalyzer_client = boto3.client('accessanalyzer')

def get_local_policies(prefix=None):
    """ローカルスコープのIAMポリシーを取得。prefixがあればフィルタ、なければ全件"""
    policies = iam_resource.policies.filter(Scope='Local')
    if prefix:
        return [p for p in policies if p.policy_name.startswith(prefix)]
    return list(policies)

def validate_policy(policy):
    """Access Analyzerでポリシーを検証し、異常があれば結果を返す"""
    try:
        response = accessanalyzer_client.validate_policy(
            policyDocument=json.dumps(policy.default_version.document),
            policyType='IDENTITY_POLICY'
        )
        findings = response.get("findings", [])
        if findings:
            return {
                'policyName': policy.policy_name,
                'policyArn': policy.arn,
                'findings': findings
            }
    except ClientError as error:
        logger.error(f"Error validating policy {policy.policy_name}: {error}")
    return None

def lambda_handler(event, context):
    prefix = 'jam-' # Lambdaイベントからprefix取得（オプション）
    abnormal_policies = []

    policies = get_local_policies(prefix)
    for p in policies:
        result = validate_policy(p)
        if result:
            abnormal_policies.append(result)

    if abnormal_policies:
        print(json.dumps(abnormal_policies))
    else:
        print('No findings !')
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# LambdaのIAMロールに以下権限が必要
# "iam:ListPolicies",
# "iam:GetPolicyVersion",
# "iam:GetPolicy",
# "access-analyzer:ValidatePolicy"