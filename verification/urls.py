from django.urls import path
from . import views

urlpatterns = [
    path('mail/<str:otp_type>', views.MailOPTCreateView.as_view(), name='mail_otp'),
]
