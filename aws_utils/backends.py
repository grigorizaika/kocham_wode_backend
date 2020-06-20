from botocore.exceptions import ClientError
from django_cognito_jwt.validator import TokenValidator, TokenError
from django.conf import settings
from django.contrib.auth import get_user_model

from .cognito import get_tokens

class CognitoBackend():
    def authenticate(self, request, username=None, password=None):
        try:
            auth_response = get_tokens(username, password)
            id_token = auth_response['AuthenticationResult']['IdToken']
        except ClientError:
            return None
        # TODO: except KeyError (when not ordinary InitiateAuth response)

        token_validator = self.get_token_validator()

        try:
            payload = token_validator.validate(id_token)
        except TokenError:
            return 

        # TODO: consider if it may be better to user attribute
        # mapping instead of letting the user handling it themselves
        user = get_user_model().objects.get_or_create_for_cognito(payload)
    
        return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_token_validator(self):
        return TokenValidator(
            settings.COGNITO_AWS_REGION,
            settings.COGNITO_USER_POOL,
            settings.COGNITO_AUDIENCE,
        )