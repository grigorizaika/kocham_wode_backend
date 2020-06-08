import boto3

from botocore.exceptions import ClientError
from django_cognito_jwt import JSONWebTokenAuthentication
from django.conf import settings



def get_client():
    return boto3.client(
        'cognito-idp',
        region_name=settings.COGNITO_AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

def get_cognito_user(email):
    return (get_client()
            .admin_get_user(
                UserPoolId=settings.COGNITO_USER_POOL_ID,
                Username=email))

def create_cognito_user(username, password, additional_attributes):
    client = get_client()

    user_attributes = [
        {'Name': k, 'Value': v} 
        for k, v in additional_attributes.items()
    ]

    return client.sign_up(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        Username=username,
        Password=password,
        UserAttributes=user_attributes)

def delete_cognito_user(username):
    client = get_client()

    return client.admin_delete_user(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=username)

def get_tokens(username, password):
    client = get_client()

    return client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password,
        },
        ClientId=settings.COGNITO_APP_CLIENT_ID,
    )

def refresh_id_token(refresh_token):
    client = get_client()

    return client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token
        },
        ClientId=settings.COGNITO_APP_CLIENT_ID,
    )

def get_user_by_token(request, token):
    auth = JSONWebTokenAuthentication()
    # TODO: request is not really needed here
    jwt_payload = auth.get_token_validator(request).validate(token)
    user = (auth.get_user_model().objects
            .get_or_create_for_cognito(jwt_payload))
    return user

def confirm_sign_up(username, confirmation_code):
    client = get_client()

    response = client.confirm_sign_up(
        ClientId=settings.COGNITO_USER_POOL_ID,
        Username=username,
        ConfirmationCode=confirmation_code,
    )

    return response

def change_password(username, old_password, new_password, access_token):
    client = get_client()
    
    response = client.change_password(
        PreviousPassword=old_password,
        ProposedPassword=new_password,
        AccessToken=access_token
    )

    return response

    

def assertCognitoUserExists(email):
    try:
        return get_cognito_user(email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            raise AssertionError(
                f"""No {email} in \
                    {settings.COGNITO_USER_POOL_ID} user pool.""")
        else:
            raise e

    @staticmethod
    def assertCognitoUserDoesntExist(email):
        try:
            get_cognito_user(email)
            raise AssertionError(
                f"""{email} exists in \
                    {settings.COGNITO_USER_POOL_ID} user pool.""")
        except ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                return
            else:
                raise e

