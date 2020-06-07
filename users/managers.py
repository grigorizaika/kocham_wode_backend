import boto3
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

from aws_utils.cognito import create_cognito_user

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_base_user(self, email, name, surname, password=None):
        # try without this
        if not email:
            raise ValueError('An email address is required')
        
        user = self.model(email=self.normalize_email(email),
                          name=name,
                          surname=surname)
        user.set_password(password)
        user.save()

        return user
    
    def _create_cognito_user(self, email, password):
        cognito_response = create_cognito_user(
            username=email, 
            password=password,
            email=email)
        
        return cognito_response

    def create_user(self, email, name, surname, password=None):
        user = self._create_base_user(email, name, surname, password)
        self._create_cognito_user(email, password)

        return user

    def create_superuser(self, email, name, surname, password=None):
        user = self._create_base_user(email, name, surname, password)
        self._create_cognito_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

    def get_or_create_for_cognito(self, payload):
        # TODO: remove print statement
        print('Payload:', payload)

        try:
            return self.get(email=payload['email'])
        except self.model.DoesNotExist:
            return self._create_base_user(
                email=payload['email'], 
                name=payload.get('given_name', None),
                surname=payload.get('family_name', None))

        

