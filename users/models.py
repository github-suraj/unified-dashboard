import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage, FileSystemStorage

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
    # image = models.ImageField(default='default.jpg', storage=OverwriteAvatar(), upload_to=upload_user_avatar)
    image = models.ImageField(default='default.jpg', upload_to=upload_user_avatar)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image and this.image != 'default.jpg':
                this.image.delete()
        except:
            pass
        super(Profile, self).save(*args, **kwargs)

        image = Image.open(self.image)
        resized_image = image.resize((300, 300), Image.ANTIALIAS)

        fh = default_storage.open(self.image.name, "wb")
        resized_image.save(fh, 'png')
        fh.close()
