from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Platform)
admin.site.register(models.Priority)
admin.site.register(models.Status)
admin.site.register(models.Issue)
admin.site.register(models.IssueComment)
admin.site.register(models.Query)
admin.site.register(models.QueryComment)
admin.site.register(models.Feedback)
admin.site.register(models.FeedbackComment)
