from datetime import datetime
from django.db import models

class Drink(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    when = models.DateTimeField(default=datetime.now, blank=False)
    vol = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.vol} ml, {self.when}, {self.user}'