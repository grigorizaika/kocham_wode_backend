from django.db.models import signals
from django.dispatch import receiver

from .models import User
from preferences.models import Preferences


@receiver(signals.post_save, sender=User)
def create_and_set_user_preferences(sender, instance, created, **kwargs):
    if created:
        preferences = Preferences.objects.create()
        instance.preferences = preferences
        instance.save()


@receiver(signals.post_delete, sender=User)
def delete_user_preferences(sender, instance, **kwargs):
    instance.preferences.delete()

