import os
from users.forms import UserDeleteForm


def global_variables(request):
    variables = {
        'du_form': UserDeleteForm(),
        'mysite': 'Go Profile',
        'env' : os.environ['ENVIRONMENT'],
    }
    return variables
