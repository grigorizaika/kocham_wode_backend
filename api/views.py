import traceback

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .serializers import PasswordSerializer
from aws_utils import cognito as cognito_helper
from users.serializers import UserSerializer


@api_view(['POST'])
@authentication_classes([])
#TODO: @required_body_params(['username', 'password'])
def get_jwt_tokens(request, **kwargs):
    try:
        auth_response = cognito_helper.get_tokens(
            request.data['username'], 
            request.data['password']
        )
        id_token = auth_response['AuthenticationResult'].get('IdToken')
        user = cognito_helper.get_user_by_token(request, id_token)

        response = {
            'auth_response': auth_response,
            'user': UserSerializer(user).data
        }

        return Response(response)
    except KeyError:
        if auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            response = {
                'auth_response': auth_response
            }
            return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        response = {f'{e.__class__.__name__}': str(e)}
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([])
# TODO: @required_body_params(['refresh_token'])
def refresh_jwt_tokens(request, *args, **kwargs):
    refresh_token = request.data['refresh_token']

    try:
        auth_response = cognito_helper.refresh_id_token(refresh_token)
        id_token = auth_response['AuthenticationResult'].get('IdToken')

    except Exception as e:
        response = {f'{e.__class__.__name__}': str(e)}
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = cognito_helper.get_user_by_token(request, id_token)

        response = {
            'auth_response': auth_response,
            'user': UserSerializer(user).data
        }

        return Response(response)
    
    except Exception as e:
        response = {f'{e.__class__.__name__}': str(e)}
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    return Response(response)


@api_view(['POST'])
# @authentication_classes([])
# @permission_classes([])
# TODO: @required_body_params(['confirmation_code', 'email'])
def confirm_sign_up(request, **kwargs):
    try:
        cognito_response = cognito_helper.confirm_sign_up(
            username=request.data['email'],
            confirmation_code=request.data['code']
        )
        response = {
            'cognito_response': cognito_response
        }
        return Response(response)
    except Exception as e:
        response = { f'{e.__class__.__name__}': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# TODO: @required_body_params(['username'])
def resend_confirmation_code(request, **kwargs):
    try:
        response = cognito_helper.resend_confirmation_code(
            request.data['username'])
    except Exception as e:
        response = { f'{e.__class__.__name__}': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# TODO: @required_body_params(['old_password', 'new_password', 'access_token'])
def change_password(request, **kwargs):
    user = request.user

    serializer = PasswordSerializer(data=request.data)

    if serializer.is_valid():
        if not user.check_password(serializer.data['old_password']):
            response = {
                'response': 'Old password didn\'t match'
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        try:
            user.set_password(serializer.data['new_password'])

            cognito_response = cognito_helper.change_password(
                request.user.email,
                serializer.data['old_password'],
                serializer.data['new_password'],
                request.data['access_token']
            )
        except Exception as e:
            response = {
                f'{e.__class__.__name__}': str(e),
                'traceback': traceback.format_stack()
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        user.save()

        response = {
            'django_response': f'Password changed for {request.user.email}',
            'cognito_response': cognito_response
        }

        return Response(response, status=status.HTTP_200_OK)

    else:
        response = {
            'errors': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
