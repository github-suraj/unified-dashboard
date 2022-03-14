from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .forms import LoginForm

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', LoginView.as_view(template_name='users/signin.html', redirect_authenticated_user=True, authentication_form=LoginForm), name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.delete_account, name='delete_account'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('change_password/', views.MyPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', views.MyPasswordResetView.as_view(), {'redirect_authenticated_user': True}, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]