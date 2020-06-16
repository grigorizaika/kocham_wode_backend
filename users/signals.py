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


# NOTE: automatic cognito user deletion is disabled 
# due to the fact that there may be users on other servers
# connected to this cognito user.
# TODO: create some sort of user count attribute, query fot it 
# at the time of deletion and if it is 1, then delete the cognito
# user also
#@receiver(signals.post_delete, sender=User)
def delete_cognito_user(sender, instance, **kwargs):
    try:
        return utils_delete_cognito_user(instance.email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # TODO: remove pring statement
            print(e, 'Resuming...')
        else:
            raise e