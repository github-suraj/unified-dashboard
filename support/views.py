from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from . import models

# Create your views here.
class IssueCreateView(LoginRequiredMixin, CreateView):
    legend = 'Report Your Issue'
    model = models.Issue
    template_name = 'support/create.html'
    fields = ('category', 'platform', 'short_description', 'long_description', 'image')

    def get_context_data(self, **kwargs):
        context = super(IssueCreateView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['long_description'].widget = forms.Textarea(attrs={'rows': 5})
        form.fields['long_description'].label = 'Long Description'
        form.fields['short_description'].label = 'Short Description'
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QueryCreateView(LoginRequiredMixin, CreateView):
    legend = 'Ask Your Query'
    model = models.Query
    template_name = 'support/create.html'
    fields = ('category', 'title', 'description')

    def get_context_data(self, **kwargs):
        context = super(QueryCreateView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].widget = forms.Textarea(attrs={'rows': 5})
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    legend = 'Submit Your Feedback'
    model = models.Feedback
    template_name = 'support/create.html'
    fields = ('category', 'description')

    def get_context_data(self, **kwargs):
        context = super(FeedbackCreateView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].widget = forms.Textarea(attrs={'rows': 5})
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
