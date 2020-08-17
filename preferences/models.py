from decimal import Decimal
from django.db import models
from users.models import User


class Preferences(models.Model):
    age = models.PositiveIntegerField(default=None, blank=True, null=True)
    weight = models.PositiveIntegerField(default=None, blank=True, null=True)
    cup_vol = models.PositiveIntegerField(default=200)
    height = models.PositiveIntegerField(default=None, blank=True, null=True)
    is_male = models.BooleanField(default=None, blank=True, null=True)
    user =  models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'pref. {self.pk} for {self.user}'

    class Meta:
        verbose_name_plural = 'Preferences'