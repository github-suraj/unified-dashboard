import os
from django.conf import settings
from users.forms import UserDeleteForm
from blogs.forms import CategoryCreateForm, BlogCommentForm
from blogs.models import Category
from support.models import Category as ServiceCategory, Priority, Status


otp_type_task_mapping = {
    'signin' : 'Login to you account',
    'signup' : 'Create new account',
}


def global_variables(request):
    variables = {
        'paginate_by': 3,
        'blog_comment_form': BlogCommentForm(),
        'category_create_form': CategoryCreateForm(),
        'user_delete_form': UserDeleteForm(),
        'blog_categories': sorted(['All'] + [category[0] for category in Category.objects.distinct().values_list('name')]),
        'service_categories': sorted(['All'] + [category[0] for category in ServiceCategory.objects.distinct().values_list('name')]),
        'service_priorities': sorted(['All'] + [category[0] for category in Priority.objects.distinct().values_list('name')]),
        'service_statuses': sorted(['All'] + [category[0] for category in Status.objects.distinct().values_list('name')]),
        'mysite': 'Go Profile',
        'mailto': settings.EMAIL_HOST_USER,
        'env' : os.environ['ENVIRONMENT'],
        'close_status_list': ('CLOSED', 'RESOLVED', 'CANCELLED')
    }
    return variables
