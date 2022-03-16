from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Category
from .forms import BlogCreateForm, CategoryCreateForm
from users.context_processors import global_variables


# Create your views here.
class UserBlogListView(ListView):
    template_name = 'blogs/user_blogs.html'
    context_object_name = 'blogs'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_queryset(self):
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except:
            messages.error(self.request, f"User with username [ {self.kwargs.get('username')} ] does not exists")
            return list()
        else:
            if user == self.request.user:
                return Blog.objects.filter(author=user).order_by('-date_posted')
            else:
                return Blog.objects.filter(author=user).filter(private=False).order_by('-date_posted')


class BLogDetailView(DetailView):
    model = Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogCreateForm
    template_name = 'blogs/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_blogs', kwargs={'username': self.request.user.username})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogCreateForm
    template_name = 'blogs/update.html'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def get_success_url(self):
        return reverse('user_blogs', kwargs={'username': self.request.user.username})


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model  = Blog
    http_method_names = ['post']

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def get_success_url(self):
        return reverse('user_blogs', kwargs={'username': self.request.user.username})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if Category.objects.filter(name=category_name).exists():
                messages.error(request, f"Category [ {category_name} ] already exists")
            else:
                form.save()
                messages.success(request, f"New Category [ {category_name} ] Added")
        return redirect('/blogs/create')
    else:
        return render(request, 'errors.html', {'err_code': 405, 'err_type': 'Method Not Allowed'})
