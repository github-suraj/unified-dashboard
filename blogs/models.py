from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('create_blog')


class Blog(models.Model):
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    private = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('create_blog')


class BlogComment(models.Model):
    comment = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)
    blog = models.ForeignKey(Blog, related_name='comment', on_delete=models.CASCADE)
    critic = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blog.category} - {self.blog.title} - {self.critic}"


class LikeBlog(models.Model):
    blog = models.OneToOneField(Blog, related_name='likes', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='blog_likes')

    def __str__(self):
        return self.blog.title


class DisLikeBlog(models.Model):
    blog = models.OneToOneField(Blog, related_name='dis_likes', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='blog_dis_likes')

    def __str__(self):
        return self.blog.title
