from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog, LikeBlog, DisLikeBlog


@receiver(post_save, sender=Blog)
def initial_blog_vote(sender, instance, created, **kwargs):
    if created:
        LikeBlog.objects.create(blog=instance)
        DisLikeBlog.objects.create(blog=instance)
