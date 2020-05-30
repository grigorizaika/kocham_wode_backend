from rest_framework import serializers

from .models import Preferences


class PreferencesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user_id(self, obj):
        return obj.get_user()

    class Meta:
        model = Preferences
        fields = ['age', 'weight', 'cup_vol', 'user',]