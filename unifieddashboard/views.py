from django.shortcuts import render
from django.views.generic import ListView
from blogs.models import Blog
from users.context_processors import global_variables


class BlogListView(ListView):
    template_name = 'home.html'
    context_object_name = 'blogs'

    @property
    def paginate_by(self):
        return global_variables(self.request)['paginate_by']

    def get_queryset(self):
        return Blog.objects.filter(private=False).order_by('-date_posted')


def handle_404(request, exception):
    context = {'err_code': 404, 'err_type': 'Page not found'}
    return render(request, 'errors.html', context)


def handle_403(request, exception):
    context = {'err_code': 403, 'err_type': 'PermissionDenied'}
    return render(request, 'errors.html', context)


def handle_500(request):
    context = {'err_code': 500, 'err_type': 'Internal Server Error'}
    return render(request, 'errors.html', context)
