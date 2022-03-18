import os
from users.forms import UserDeleteForm
from blogs.forms import CategoryCreateForm, BlogCommentForm
from blogs.models import Category


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
        'mysite': 'Go Profile',
        'env' : os.environ['ENVIRONMENT'],
    }
    return variables
