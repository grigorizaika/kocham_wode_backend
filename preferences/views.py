from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Preferences
from .serializers import PreferencesSerializer


class PreferencesView(APIView):
    def get_all_preferences(self, serialized=True):
        all_preferences = Preferences.objects.all()

        if serialized:
            all_preferences = PreferencesSerializer(
                all_preferences, many=True).data
        
        return all_preferences

    def get_preferences_by_id(self, id, serialized=True):
        preferences = Preferences.objects.get(pk=id)

        if serialized:
            preferences = PreferencesSerializer(preferences).data

        return preferences

    def get_preferences_by_user_id(self, user_id, serialized=True):
        preferences = Preferences.objects.get(user=user_id)

        if serialized:
            preferences = PreferencesSerializer(preferences).data

        return preferences

    def update_preferences(self, preferences, data):
        serializer = PreferencesSerializer(
            preferences, data=data, partial=True)

        if serializer.is_valid():
            preferences = serializer.save()
            return preferences
        else:
            raise ValueError(serializer.errors)

    def update_preferences_by_id(self, id, data):
        preferences = self.get_preferences_by_id(id, serialized=False)
        preferences = self.update_preferences(preferences, data)
        return preferences

    def update_preferences_by_user_id(self, user_id, data):
        preferences = self.get_preferences_by_user_id(
            user_id, serialized=False)
        preferences = self.update_preferences(preferences, data)
        return preferences

    def delete_preferences_by_id(self, id):
        self.get_preferences_by_id(id, serialized=False).delete()
        return id

    def delete_preferences_by_user_id(self, user_id):
        preferences = self.get_preferences_by_user_id(
            user_id, serialized=False)
        id = preferences.id
        preferences.delete()
        return id

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            try:
                preferences = self.get_preferences_by_id(kwargs['id'])
            except Preferences.DoesNotExist as dne:
                if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {'preferences': 'Permission denied'}
                    return Response(response, status=status.HTTP_403_FORBIDDEN)

            if (preferences['user'] == request.user.id
                    or request.user.is_staff):
                response = {'preferences': preferences}
                return Response(response)
            else:
                response = {'preferences': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

        if 'user_id' in kwargs:
            if (kwargs['user_id'] != request.user.id
                    and not request.user.is_staff):
                response = {'users': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            try:
                preferences = self.get_preferences_by_user_id(kwargs['user_id'])
            except Preferences.DoesNotExist as dne:
                if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {'users': 'Permission denied'}
                    return Response(response, status=status.HTTP_403_FORBIDDEN)

            response = {'preferences': preferences}
            return Response(response)

        if request.user.is_staff:
            all_preferences = self.get_all_preferences()
            response = {'preferences': all_preferences}
            return Response(response)

        else:
            response = {'preferences': 'Permission denied'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    
    def patch(self, request, *args, **kwargs):
        data = request.data

        if 'id' in kwargs:
            try:
                preferences = self.update_preferences_by_id(kwargs['id'], data)
            except Preferences.DoesNotExist as dne:
                if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {'preferences': 'Permission denied'}
                    return Response(response, status=status.HTTP_403_FORBIDDEN)

            if (preferences.user == request.user.id
                    or request.user.is_staff):
                response = {'preferences': f'Updated preferences {preferences.id}'}
                return Response(response)
            else:
                response = {'preferences': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

        if 'user_id' in kwargs:
            if (kwargs['user_id'] != request.user.id
                    and not request.user.is_staff):
                response = {'users': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            try:
                preferences = self.update_preferences_by_user_id(kwargs['user_id'], data)
            except Preferences.DoesNotExist as dne:
                if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {'users': 'Permission denied'}
                    return Response(response, status=status.HTTP_403_FORBIDDEN)

            response = {'preferences': f'Updated preferences {preferences.id}'}
            return Response(response)

        response = {'preferences': 'ID not specified'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if 'id' in kwargs:
            try:
                preferences = self.delete_preferences_by_id(kwargs['id'])
            except Preferences.DoesNotExist as dne:
                if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {'preferences': 'Permission denied'}
                    return Response(response, status=status.HTTP_403_FORBIDDEN)

            if (preferences['user'] == request.user.id
                    or request.user.is_staff):
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            else:
                response = {'preferences': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

        if 'user_id' in kwargs:
            if (kwargs['user_id'] != request.user.id
                    and not request.user.is_staff):
                response = {'users': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            try:
                preferences = self.delete_preferences_by_user_id(kwargs['user_id'])
            except Preferences.DoesNotExist as dne:
                if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {'users': 'Permission denied'}
                    return Response(response, status=status.HTTP_403_FORBIDDEN)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        response = {'preferences': 'ID not specified'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)