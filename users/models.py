import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.
def upload_user_avatar(instance, filename):
    file_ext = os.path.splitext(filename)[-1]
    file_name = instance.user.username + file_ext
    return os.path.join('avatars', file_name)


class OverwriteAvatar(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


class Profile(models.Model):
    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ]
    )
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(default='default.jpg', storage=OverwriteAvatar(), upload_to=upload_user_avatar)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
