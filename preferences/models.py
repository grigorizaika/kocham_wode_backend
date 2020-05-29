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

    def get_user(self):
        try:
            return User.objects.get(preferences=self)
        except User.DoesNotExist:
            return None

    def __str__(self):
        return f'pref. {self.pk} for {self.get_user()}'

    
    class Meta:
        verbose_name_plural = 'Preferences'