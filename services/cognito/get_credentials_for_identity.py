
import boto3
import os
import json

USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
ID_POOL_ID = os.environ['ID_POOL_ID']
REGION  = os.environ['REGION']

cognito = boto3.client('cognito-idp', region_name=REGION)
cognito_identity = boto3.client('cognito-identity', region_name=REGION)

def cognito_auth(username, password):
	# 認証開始
	try:
		aws_result = cognito.admin_initiate_auth(
			UserPoolId = USER_POOL_ID,
			ClientId = CLIENT_ID,
			AuthFlow = "ADMIN_NO_SRP_AUTH",
			AuthParameters = {
				"USERNAME": username,
				"PASSWORD": password,
			}
		)
		# 認証完了
		return aws_result

	except Exception as e :
		# 認証失敗
		print(e)
		return None

def get_id(identity_pool_id, id_token):
    logins_key = f"cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"
    response = cognito_identity.get_id(
        IdentityPoolId=identity_pool_id,
        Logins = {
            logins_key: id_token
        }
    )

    return response


def get_credentials_for_identity(identity_id, id_token):
    logins_key = f"cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"

    response = cognito_identity.get_credentials_for_identity(
        IdentityId = identity_id,
        Logins = {
            logins_key: id_token
        }
    )
    return response

# Lambdaハンドラー
def lambda_handler(event, context):
    try:
        username = 'user01'
        password = 'P@ssw0rda'

        authentication_result = cognito_auth(username, password)

        if authentication_result:
            id_token = authentication_result["AuthenticationResult"]["IdToken"]
            identity_id = get_id(ID_POOL_ID, id_token)['IdentityId']

            credentials_response = get_credentials_for_identity(identity_id, id_token)
            session = boto3.Session(
                aws_access_key_id=credentials_response['Credentials']['AccessKeyId'],
                aws_secret_access_key=credentials_response['Credentials']['SecretKey'],
                aws_session_token=credentials_response['Credentials']['SessionToken'],
            )

            dynamodb = session.client('dynamodb', region_name=REGION)
            statusCode = 200
            response_body = dynamodb.scan(TableName='sample-table')

        else:
            statusCode = 401
            response_body = '認証に失敗しました。'
    except Exception as e:
        print(e)
        statusCode = 500
        response_body = '処理に失敗しました。'

    return {
        'statusCode': statusCode,
        'body': json.dumps(response_body, default=str, ensure_ascii=False)
    }