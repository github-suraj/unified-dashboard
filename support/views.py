from django import forms
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
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
        if self.request.method == 'GET' and self.request.user.is_superuser:
            return True
        elif self.request.method == 'POST' and self.request.user.is_superuser:
            return True if self.get_object().status.name not in global_variables(self.request)['close_status_list'] else False
        return False


class IssueListView(LoginRequiredMixin, ListView):
    legend = 'Reported Issues'
    create_url = 'submit_issue'
    update_url = 'update_issue'
    details_url = 'issue_details'
    template_name = 'support/services.html'
    context_object_name = 'objects'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend, 'create_url': self.create_url, 'update_url': self.update_url ,'details_url': self.details_url})
        return context

    def get_queryset(self):
        if self.request.GET.get('admin') == 'true' and self.request.user.is_superuser:
            queryset = models.Issue.objects.all().order_by('-create_date')
        else:
            queryset = models.Issue.objects.filter(author=self.request.user).order_by('-create_date')

        if self.request.GET.get('category', 'All') != 'All':
            category = get_object_or_404(models.Category, name=self.request.GET['category'])
            queryset = queryset.filter(category=category)
        if self.request.GET.get('status', 'All') != 'All':
            status = get_object_or_404(models.Status, name=self.request.GET['status'])
            queryset = queryset.filter(status=status)
        if self.request.GET.get('priority', 'All') != 'All':
            priority = get_object_or_404(models.Priority, name=self.request.GET['priority'])
            queryset = queryset.filter(priority=priority)
        return queryset


class QueryListView(LoginRequiredMixin, ListView):
    legend = 'All Queries'
    create_url = 'submit_query'
    update_url = 'update_query'
    details_url = 'query_details'
    template_name = 'support/services.html'
    context_object_name = 'objects'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_context_data(self, **kwargs):
        context = super(QueryListView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend, 'create_url': self.create_url, 'update_url': self.update_url ,'details_url': self.details_url})
        return context

    def get_queryset(self):
        if self.request.GET.get('admin') == 'true' and self.request.user.is_superuser:
            queryset = models.Query.objects.all().order_by('-open_date')
        else:
            queryset = models.Query.objects.filter(author=self.request.user).order_by('-open_date')

        if self.request.GET.get('category', 'All') != 'All':
            category = get_object_or_404(models.Category, name=self.request.GET['category'])
            queryset = queryset.filter(category=category)
        if self.request.GET.get('status', 'All') != 'All':
            status = get_object_or_404(models.Status, name=self.request.GET['status'])
            queryset = queryset.filter(status=status)
        return queryset


class FeedbackListView(LoginRequiredMixin, ListView):
    legend = 'Suggestions / Feedback'
    create_url = 'submit_feedback'
    update_url = 'update_feedback'
    details_url = 'feedback_details'
    template_name = 'support/services.html'
    context_object_name = 'objects'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_context_data(self, **kwargs):
        context = super(FeedbackListView, self).get_context_data(**kwargs)
        context.update({'legend': self.legend, 'create_url': self.create_url, 'update_url': self.update_url ,'details_url': self.details_url})
        return context

    def get_queryset(self):
        if self.request.GET.get('admin') == 'true' and self.request.user.is_superuser:
            queryset = models.Feedback.objects.all().order_by('-date_posted')
        else:
            queryset = models.Feedback.objects.filter(author=self.request.user).order_by('-date_posted')

        if self.request.GET.get('category', 'All') != 'All':
            category = get_object_or_404(models.Category, name=self.request.GET['category'])
            queryset = queryset.filter(category=category)
        return queryset


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
        if self.request.method == 'GET' and self.request.user.is_superuser:
            return True
        elif self.request.method == 'POST' and self.request.user.is_superuser:
            return True if not self.get_object().actioned else False
        return False

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
