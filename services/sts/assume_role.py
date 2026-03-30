import boto3
from boto3.session import Session

# 異なるAWSアカウント/ロールのクレデンシャル取得を実行する
def sts_assume_role(account_id,role_name):
    role_arn = "arn:aws:iam::" + account_id + ":role/" + role_name
    session_name = "foobar"
    region = "ap-northeast-1"

    client = boto3.client('sts')

    # AssumeRoleで一時クレデンシャルを取得
    response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )

    session = Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'],
        region_name=region
    )

    return session

def scan_cross_account(session):
    # 新しく発行したsessionを使って実行する
    dynamodb = session.client("dynamodb")
    table = 'sample-table'
    response = dynamodb.scan(TableName=table)
    return response['Items']

def lambda_handler(event,context):
    account_id = '<cross_account_id>'
    role_name = '<cross_account_role_name>'

    # イベントで指定されたAWSアカウント/ロールのクレデンシャルを取得
    session = sts_assume_role(account_id,role_name)

    scan_response = scan_cross_account(session)

    return scan_response