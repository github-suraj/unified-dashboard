from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email id")
    first_name = forms.CharField(max_length=200, required=True, help_text="200 characters or fewer.")
    last_name = forms.CharField(max_length=200, required=True, help_text="200 characters or fewer.")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        _user = User.objects.get(username=user.username)
        _user.is_active = True
        _user.save()
        return super().confirm_login_allowed(_user)


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(required=True, help_text="Enter a valid email id")
    first_name = forms.CharField(max_length=200, required=True, help_text="200 characters or fewer.")
    last_name = forms.CharField(max_length=200, required=True, help_text="200 characters or fewer.")

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except:
            return self.cleaned_data['email']

        if user.username != self.request.user.username:
            raise forms.ValidationError("A user with that email already exists.")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'dob', 'image']
        widgets = {
            'dob': DateInput(),
        }
