from django import forms
from .models import MailOTP

class MailOTPForm(forms.ModelForm):
    class Meta:
        model = MailOTP
        fields = ['email']
