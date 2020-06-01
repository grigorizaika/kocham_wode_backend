from django.db.models import signals
from django.dispatch import receiver

from .models import User
from preferences.models import Preferences


@receiver(signals.post_save, sender=User)
def create_and_set_user_preferences(sender, instance, created, **kwargs):
    if created:
        preferences = Preferences.objects.create(user=instance)


# NOTE: should this be here at all? 
# Or should both the creation and the deletion be in views?
@receiver(signals.post_delete, sender=User)
def delete_cognito_user(sender, instance, **kwargs):
    pass