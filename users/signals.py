from botocore.exceptions import ClientError
from django.db.models import signals
from django.dispatch import receiver

from .models import User
from aws_utils.cognito import delete_cognito_user as utils_delete_cognito_user
from preferences.models import Preferences


@receiver(signals.post_save, sender=User)
def create_and_set_user_preferences(sender, instance, created, **kwargs):
    if created:
        preferences = Preferences.objects.create(user=instance)


# NOTE: should this be here at all? 
# Or should both the creation and the deletion be in views?
@receiver(signals.post_delete, sender=User)
def delete_cognito_user(sender, instance, **kwargs):
    try:
        return utils_delete_cognito_user(instance.email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # TODO: remove pring statement
            print(e, 'Resuming...')
        else:
            raise e