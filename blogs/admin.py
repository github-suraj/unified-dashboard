from django.contrib import admin
from .models import Category, Blog, BlogComment, LikeBlog, DisLikeBlog

# Register your models here.
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(LikeBlog)
admin.site.register(DisLikeBlog)
