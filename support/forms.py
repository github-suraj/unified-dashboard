from django import forms
from . import models

class IssueCommentForm(forms.ModelForm):
    class Meta:
        model = models.IssueComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1}),
        }


class QueryCommentForm(forms.ModelForm):
    class Meta:
        model = models.QueryComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1}),
        }


class FeedbackCommentForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1}),
        }
