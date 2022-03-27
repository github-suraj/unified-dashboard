from django import forms
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models
from .forms import FeedbackCommentForm, IssueCommentForm, QueryCommentForm
from users.context_processors import global_variables


# Create your views here.
class SupportUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user == self.get_object().author or self.request.user.is_superuser:
            return True
        return False


class UpdateUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().status.name in global_variables(self.request)['close_status_list'] and self.request.method == 'POST':
            return False
        return True


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


class IssueUpdateView(LoginRequiredMixin, UpdateUserPassesTestMixin, UpdateView):
    model = models.Issue
    legend = 'Issue'
    details_url = 'issue_details'
    template_name = 'support/update.html'
    fields = ('priority', 'due_date', 'status', 'close_date')
    
    def get_success_url(self):
        return reverse('issue_details', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(IssueUpdateView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend, 'details_url': self.details_url})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        form.fields['close_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        return form


class QueryUpdateView(LoginRequiredMixin, UpdateUserPassesTestMixin, UpdateView):
    model = models.Query
    legend = 'Query'
    details_url = 'query_details'
    template_name = 'support/update.html'
    fields = ('status', 'close_date')
    
    def get_success_url(self):
        return reverse('query_details', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(QueryUpdateView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend, 'details_url': self.details_url})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['close_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        return form


class FeedbackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Feedback
    legend = 'Feedback'
    details_url = 'feedback_details'
    template_name = 'support/update.html'
    fields = ('actioned', 'date_actioned')
    
    def get_success_url(self):
        return reverse('feedback_details', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(FeedbackUpdateView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend, 'details_url': self.details_url})
        return context

    def test_func(self):
        if self.get_object().actioned == True and self.request.method == 'POST':
            return False
        return True

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_actioned'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        return form


class IssueDetailView(LoginRequiredMixin, SupportUserPassesTestMixin, DetailView):
    model = models.Issue
    template_name = 'support/issue_detail.html'


class QueryDetailView(LoginRequiredMixin, SupportUserPassesTestMixin, DetailView):
    model = models.Query
    template_name = 'support/query_detail.html'


class FeedbackDetailView(LoginRequiredMixin, SupportUserPassesTestMixin, DetailView):
    model = models.Feedback
    template_name = 'support/feedback_detail.html'


class IssueCommentCreateView(LoginRequiredMixin, CreateView):
    model = models.IssueComment
    form_class = IssueCommentForm
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('issue_details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.issue_id = self.kwargs['pk']
        form.instance.critic = self.request.user
        return super().form_valid(form)


class QueryCommentCreateView(LoginRequiredMixin, CreateView):
    model = models.QueryComment
    form_class = QueryCommentForm
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('query_details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.query_id = self.kwargs['pk']
        form.instance.critic = self.request.user
        return super().form_valid(form)


class FeedbackCommentCreateView(LoginRequiredMixin, CreateView):
    model = models.FeedbackComment
    form_class = FeedbackCommentForm
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('feedback_details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.feedback_id = self.kwargs['pk']
        form.instance.critic = self.request.user
        return super().form_valid(form)
