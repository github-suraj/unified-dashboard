import os
import re
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
def upload_issue_images(instance, filename):
    file_ext = os.path.splitext(filename)[-1]
    ref_title = re.sub('\W', '', instance.short_description)[:50]
    file_name = f"{instance.author.username}_{ref_title}_{instance.create_date.timestamp()}" + file_ext
    return os.path.join('support', instance.category.name.replace(' ', ''), file_name)


def default_user():
    return User.objects.get(username='deleted')


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=10)

    @classmethod
    def get_default_status(cls):
        status, created = cls.objects.get_or_create(name='OPEN')
        return status.pk

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=10)

    @classmethod
    def get_default_priority(cls):
        priority, created = cls.objects.get_or_create(name='LOW')
        return priority.pk

    def __str__(self):
        return self.name


class Issue(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    platform = models.ForeignKey(Platform, on_delete=models.RESTRICT)
    priority = models.ForeignKey(Priority, on_delete=models.RESTRICT, default=Priority.get_default_priority)
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    image = models.ImageField(upload_to=upload_issue_images, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, default=Status.get_default_status)

    def __str__(self):
        return f"{self.category} - {self.short_description}"

    # def save(self, *args, **kwargs):
    #     try:
    #         this = Issue.objects.get(id=self.id)
    #         if this.image != self.image:
    #             this.image.delete()
    #     except:
    #         pass
    #     super(Issue, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home')


class IssueComment(models.Model):
    comment = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)
    issue = models.ForeignKey(Issue, related_name='comment', on_delete=models.CASCADE)
    critic = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)

    def __str__(self):
        return f"{self.issue} - {self.critic}"


class Query(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(max_length=100)
    description = models.TextField()
    open_date = models.DateTimeField(default=timezone.now)
    close_date = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, default=Status.get_default_status)

    def __str__(self):
        return f"{self.category} - {self.title}"

    def get_absolute_url(self):
        return reverse('home')


class QueryComment(models.Model):
    comment = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)
    query = models.ForeignKey(Query, related_name='comment', on_delete=models.CASCADE)
    critic = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)

    def __str__(self):
        return f"{self.query} - {self.critic}"


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_actioned = models.DateTimeField(blank=True, null=True)
    actioned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} - {self.description[:50]}"

    def get_absolute_url(self):
        return reverse('home')


class FeedbackComment(models.Model):
    comment = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)
    feedback = models.ForeignKey(Feedback, related_name='comment', on_delete=models.CASCADE)
    critic = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)

    def __str__(self):
        return f"{self.feedback} - {self.critic}"
