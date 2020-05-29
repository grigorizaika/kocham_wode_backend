from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _

from .managers import CustomUserManager
from drinks.models import Drink

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    preferences = models.OneToOneField(
        'preferences.Preferences',
        on_delete=models.SET_NULL,
        null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_all_drinks(self):
        return Drink.objects.filter(user=self)

    def get_drinks_by_date(self, date):
        return Drink.objects.filter(
            when__year=date.year, 
            when__month=date.month,
            when__day=date.day
        )

    def get_drinks_by_date_range(self, date_start, date_end):
        return Drink.objects.filter(
            when__gte=date_start,
            when__lt=date_end
        )

    def get_drinks(self, date=None, date_start=None, date_end=None):
        if date:
            return self.get_drinks_by_date(date)

        if date_start and date_end:
            return self.get_drinks_by_date_range(date_start, date_end)
        
        return self.get_all_drinks()
