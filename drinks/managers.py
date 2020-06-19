from django.apps import apps
from django.db import models




class DrinkManager(models.Manager):
    def group_all_by_user(self, date=None, date_start=None, date_end=None, 
                          key_attribute='id'):
        User = apps.get_model('users.user')
        
        grouped = {}
        users = User.objects.all()

        for user in users:
            if date:
                grouped[getattr(user, key_attribute)] = user.get_drinks_by_date(date)
            elif date_start and date_end:
                grouped[getattr(user, key_attribute)] = user.get_drinks_by_date_range(
                    date_start, date_end)
            else:
                grouped[getattr(user, key_attribute)] = user.get_all_drinks()

        return grouped