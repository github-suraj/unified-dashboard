import re
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from users.context_processors import global_variables
from .models import Blog, Category, BlogComment, LikeBlog, DisLikeBlog, LikeBlogComment, DisLikeBlogComment
from .forms import BlogCreateForm, CategoryCreateForm, BlogCommentForm


# Create your views here.
class UserBlogListView(ListView):
    template_name = 'blogs/user_blogs.html'
    context_object_name = 'blogs'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_queryset(self):
        category = self.kwargs.get('category')
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'), is_active=True)
        except:
            messages.error(self.request, f"User with username [ {self.kwargs.get('username')} ] does not exists")
            return list()
        else:
            if user == self.request.user:
                query_set = Blog.objects.filter(author=user).order_by('-date_posted')
            else:
                query_set = Blog.objects.filter(author=user).filter(private=False).order_by('-date_posted')
            return query_set if not category or category == 'All' else query_set.filter(category=category)


class CategoryBlogListView(ListView):
    template_name = 'blogs/category_blogs.html'
    context_object_name = 'blogs'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_queryset(self):
        category_name = self.kwargs.get('category', 'All')
        try:
            if category_name != 'All':
                category = get_object_or_404(Category, name=category_name)
        except:
            messages.error(self.request, f"Category with name [ {self.kwargs.get('category')} ] does not exists")
            return list()
        else:
            if category_name == 'All':
                query_set = Blog.objects.filter(Q(author__in=User.objects.filter(is_active=True))).order_by('-date_posted')
            else:
                query_set = Blog.objects.filter(Q(author__in=User.objects.filter(is_active=True)) & Q(category=category)).order_by('-date_posted')

            if self.request.user.is_authenticated:
                return query_set.filter(Q(author=self.request.user) | (~Q(author=self.request.user) & Q(private=False)))
            else:
                return query_set.filter(private=False)


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
        return reverse('user_blogs', kwargs={'username': self.request.user.username, 'category': 'All'})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogCreateForm
    template_name = 'blogs/update.html'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def get_success_url(self):
        return reverse('user_blogs', kwargs={'username': self.request.user.username, 'category': 'All'})


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model  = Blog
    http_method_names = ['post']

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def get_success_url(self):
        return reverse('user_blogs', kwargs={'username': self.request.user.username, 'category': 'All'})


class BlogCommentCreateView(LoginRequiredMixin, CreateView):
    model = BlogComment
    form_class = BlogCommentForm
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('blog_details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.blog_id = self.kwargs['pk']
        form.instance.critic = self.request.user
        return super().form_valid(form)


class BlogCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogComment
    form_class = BlogCommentForm

    def test_func(self):
        if self.request.user == self.get_object().critic:
            return True
        return False

    def get_success_url(self):
        return reverse('blog_details', kwargs={'pk': self.get_object().blog.id})


class BlogCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model  = BlogComment
    http_method_names = ['post']

    def test_func(self):
        if self.request.user == self.get_object().critic:
            return True
        return False

    def get_success_url(self):
        return reverse('blog_details', kwargs={'pk': self.get_object().blog.id})


class BlogVoteView(LoginRequiredMixin, View):
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs['pk']
        opinion = self.kwargs['opinion']

        blog = get_object_or_404(Blog, id=blog_id)

        try:
            # If child Like object does not exists then create
            blog.likes
        except Blog.likes.RelatedObjectDoesNotExist as e:
            LikeBlog.objects.create(blog=blog)

        try:
            # If child DisLike object does not exists then create
            blog.dis_likes
        except Blog.dis_likes.RelatedObjectDoesNotExist as e:
            DisLikeBlog.objects.create(blog=blog)

        if opinion == 'like':
            if request.user in blog.likes.users.all():
                blog.likes.users.remove(request.user)
            else:
                blog.likes.users.add(request.user)
                blog.dis_likes.users.remove(request.user)
        elif opinion == 'dislike':
            if request.user in blog.dis_likes.users.all():
                blog.dis_likes.users.remove(request.user)
            else:
                blog.dis_likes.users.add(request.user)
                blog.likes.users.remove(request.user)

        redirect_to = request.META.get('HTTP_REFERER')
        if re.search(r'/blogs/\d+/(dis)?like/vote', redirect_to):
            return redirect(reverse('blog_details', kwargs={'pk': blog_id}))
        return HttpResponseRedirect(redirect_to)


class BlogCommentVoteView(LoginRequiredMixin, View):
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        opinion = self.kwargs['opinion']

        comment = get_object_or_404(BlogComment, id=comment_id)

        try:
            # If child Like object does not exists then create
            comment.likes
        except BlogComment.likes.RelatedObjectDoesNotExist as e:
            LikeBlogComment.objects.create(comment=comment)

        try:
            # If child DisLike object does not exists then create
            comment.dis_likes
        except BlogComment.dis_likes.RelatedObjectDoesNotExist as e:
            DisLikeBlogComment.objects.create(comment=comment)

        if opinion == 'like':
            if request.user in comment.likes.users.all():
                comment.likes.users.remove(request.user)
            else:
                comment.likes.users.add(request.user)
                comment.dis_likes.users.remove(request.user)
        elif opinion == 'dislike':
            if request.user in comment.dis_likes.users.all():
                comment.dis_likes.users.remove(request.user)
            else:
                comment.dis_likes.users.add(request.user)
                comment.likes.users.remove(request.user)

        redirect_to = request.META.get('HTTP_REFERER')
        if re.search(r'/blogs/comment/\d+/(dis)?like/vote', redirect_to):
            return redirect(reverse('blog_details', kwargs={'pk': comment.blog.id}))
        return HttpResponseRedirect(redirect_to)


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
