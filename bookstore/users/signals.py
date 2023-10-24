from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Avatar

User = get_user_model()

@receiver(post_save, sender=User)
def create_avatar(user, instance, created, **kwargs):
    if created:
        Avatar.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_avatar(sender, instance, **kwargs):
    instance.avatar.save()
