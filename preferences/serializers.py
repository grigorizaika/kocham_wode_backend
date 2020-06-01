from rest_framework import serializers

from .models import Preferences
from users.models import User

class PreferencesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Preferences
        fields = ['id', 'age', 'weight', 'cup_vol', 'user']