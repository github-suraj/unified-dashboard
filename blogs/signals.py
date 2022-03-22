from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from . import models


@receiver(post_save, sender=models.Blog)
def initial_blog_vote(sender, instance, created, **kwargs):
    if created:
        models.LikeBlog.objects.create(blog=instance)
        models.DisLikeBlog.objects.create(blog=instance)


@receiver(post_save, sender=models.BlogComment)
def initial_blog_vote(sender, instance, created, **kwargs):
    if created:
        models.LikeBlogComment.objects.create(comment=instance)
        models.DisLikeBlogComment.objects.create(comment=instance)


@receiver(pre_delete, sender=models.Blog)
def delete_blog_image(sender, instance, **kwargs):
    if instance.image:
        try:
            instance.image.delete()
        except:
            pass
