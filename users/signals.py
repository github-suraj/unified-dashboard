from django.db.models.signals import post_save, pre_delete
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import Profile


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.info(request, 'You have been logged out!')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    if instance.image and instance.image != 'default.jpg':
        try:
            instance.image.delete()
        except:
            pass
