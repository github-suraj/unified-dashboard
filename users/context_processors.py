import os
from users.forms import UserDeleteForm
from blogs.forms import CategoryCreateForm


def global_variables(request):
    variables = {
        'paginate_by': 3,
        'cc_form': CategoryCreateForm(),
        'du_form': UserDeleteForm(),
        'mysite': 'Go Profile',
        'env' : os.environ['ENVIRONMENT'],
    }
    return variables
