from rest_framework import serializers

from .models import User
from preferences.serializers import PreferencesSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'})

    def create(self, validated_data):
        
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

    def validate(self, data):
        password = data['password']
        password2 = data['password2']

        if password != password2:
            raise serializers.ValidationError('Passwords don\'t match')

        return data

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']


class UserSerializer(serializers.ModelSerializer):
    preferences = PreferencesSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'preferences']
        read_only_fields = ['preferences']