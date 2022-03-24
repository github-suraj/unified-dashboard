from blogs.models import Blog
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from users.context_processors import global_variables


class BlogListView(ListView):
    template_name = 'home.html'
    context_object_name = 'blogs'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by'] - 1

    def get_queryset(self):
        return Blog.objects.filter(Q(private=False) & Q(author__in=User.objects.filter(is_active=True))).order_by('-date_posted')


def handle_404(request, exception):
    context = {'err_code': 404, 'err_type': 'Page not found'}
    return render(request, 'errors.html', context)


def handle_403(request, exception):
    context = {'err_code': 403, 'err_type': 'PermissionDenied'}
    return render(request, 'errors.html', context)


def handle_500(request):
    context = {'err_code': 500, 'err_type': 'Internal Server Error'}
    return render(request, 'errors.html', context)
