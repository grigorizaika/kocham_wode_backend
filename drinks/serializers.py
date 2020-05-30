from rest_framework import serializers

from .model import Drink


class DrinkSerializer(serializer.ModelSerializer):

    class Meta:
        model = Drink
        fields = ['when', 'vol', 'user']
        read_only_fields = ['user']