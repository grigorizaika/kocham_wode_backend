import boto3
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

from aws_utils.cognito import create_cognito_user

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_base_user(self, email, name, password=None):
        # try without this
        if not email:
            raise ValueError('An email address is required')
        
        user = self.model(email=self.normalize_email(email),
                          name=name)
        user.set_password(password)
        user.save()

        return user
    
    def _create_cognito_user(self, email, password, attributes):
        cognito_response = create_cognito_user(
            username=email, 
            password=password,
            additional_attributes=attributes)

        return cognito_response

    def create_user(self, email, name, password=None):
        user = self._create_base_user(email, name, password)

        try:
            attributes = {
                'email': email,
                'custom:is_administrator': 'False'
            }
            self._create_cognito_user(email, password, attributes)
        except Exception as e:
            user.delete()
            raise e

        return user

    def create_superuser(self, email, name, password=None):
        user = self._create_base_user(email, name, password)
        
        try:
            attributes = {
                'email': email,
                'custom:is_administrator': 'True'
            }
            self._create_cognito_user(email, password, attributes)
        except Exception as e:
            user.delete()
            raise e

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

    def get_or_create_for_cognito(self, payload):
        try:
            return self.get(email=payload['email'])
        except self.model.DoesNotExist:
            user = self._create_base_user(
                email=payload['email'], 
                name=payload.get('given_name', None))
            is_administrator = (
                True if payload['custom:is_administrator'].lower() == "true"
                else False
                )

            if is_administrator:
                user.is_staff = True
                user.is_superuser = True
                user.save()

            return user
        

