from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Blog)
admin.site.register(models.BlogComment)
admin.site.register(models.LikeBlog)
admin.site.register(models.DisLikeBlog)
admin.site.register(models.LikeBlogComment)
admin.site.register(models.DisLikeBlogComment)
