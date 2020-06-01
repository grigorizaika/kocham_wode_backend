from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Preferences(models.Model):
    age = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(
        max_digits=4, decimal_places=1, default=0.01,
        validators=[MinValueValidator(Decimal('0.01'))])
    cup_vol = models.IntegerField(default=200)
    user =  models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'pref. {self.pk} for {self.user}'

    class Meta:
        verbose_name_plural = 'Preferences'