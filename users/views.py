from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegistrationSerializer, UserSerializer


@api_view(['POST'])
def register_user(request):
    """ 
    User registration endpoint.
    parameters: 
    email, name, surname, password, password2
    """

    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        response = {'user': f'Successfully registered {user.email}'}
        return Response(response)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    
    def get_all_users(self, serialized=False):
        all_users = User.objects.all()

        if serialized:
            all_users = UserSerializer(all_users, many=True).data

        return all_users

    def get_user_by_id(self, id, serialized=False):
        user = User.objects.get(pk=id)

        if serialized:
            user = UserSerializer(user).data
        
        return user

    def update_user(self, id, data):
        user = self.get_user_by_id(id)
        serializer = UserSerializer(user, data=data, partial=True)
        
        if serializer.is_valid():
            user = serializer.save()
            return user
        else:
            raise ValueError(serializer.errors)

    def delete_user(self, id):
        self.get_user_by_id(id).delete()
        return id

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            # TODO: move it to object-level premission logic
            if (request.user.id == kwargs['id']
                    or request.user.is_staff):
                try:
                    user = self.get_user_by_id(kwargs['id'], serialized=True)

                except User.DoesNotExist as dne:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)

                return Response(user)

            else:
                response = {'user': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
        
        if request.user.is_staff:
            all_users = self.get_all_users(serialized=True)
            return Response(all_users)

        else:
            response = {'user': 'Permission denied'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    
    #TODO: port decorators
    #@required_kwargs(['id'])
    def patch(self, request, *args, **kwargs):
        # TODO: move it to object-level premission logic
        if (request.user.id == kwargs['id']
                or request.user.is_staff):

            try:
                updated_user = self.update_user(kwargs['id'], request.data)
                response = {'user': f'Successfully updated {updated_user.email}'}
                return Response(response)

            except ValueError as ve:
                return Response(ve, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist as dne:
                return Response(dne, status=status.HTTP_404_NOT_FOUND)

        else:
            response = {'user': 'Permission denied'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
            # TODO: move it to object-level premission logic
            if (request.user.id == kwargs['id']
                    or request.user.is_staff):
                
                try:
                    self.delete_user(kwargs['id'])
                    return Response({}, status=status.HTTP_204_NO_CONTENT)

                except ValueError as ve:
                    return Response(ve, status=status.HTTP_400_BAD_REQUEST)

                except User.DoesNotExist as dne:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
