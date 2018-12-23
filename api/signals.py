from allauth.account.models import *
from django.db.models.signals import *
from django.dispatch import receiver

from api.models import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def change_user_email(sender, instance, **kwargs):
    email = instance.email
    EmailAddress.objects.create(email=email, user=instance, primary=True)
    EmailAddress.objects.filter(user=instance).exclude(email=email).delete()


@receiver(post_save, sender=User)
def set_username_equal_to_email(sender, instance, created, **kwargs):
    if created:
        instance.save(username=instance.email)
