from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from .forms import UserRegisterForm, UserDeleteForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = '/accounts/signin'

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been set! You are now able to Sign In with new password.')
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/accounts/profile')
        return super().dispatch(*args, **kwargs)


class MyPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    success_url = '/'

    def form_valid(self, form):
        messages.info(self.request, mark_safe('We have emailed you instructions for setting your password. \
            <br/>If an account exists with the email you entered. You should receive them shortly. \
            <br/>If you don\'t receive an email, please make sure you\'ve entered the address you registered with, \
            and check your spam folder.')
        )
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/accounts/profile')
        return super().dispatch(*args, **kwargs)


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = '/accounts/signin'

    def form_valid(self, form):
        form.save()
        self.request.session.flush()
        messages.success(self.request, 'Your password was successfully updated! Please sign in with new password.')
        auth.logout(self.request)
        return super().form_valid(form)


def signup(request):
    if request.user.is_authenticated:
        return redirect('/accounts/profile')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, new_user)
            messages.success(request, f'Welcome {new_user.first_name} {new_user.last_name}! Now you can update your profile.')
            return redirect('/accounts/profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def signout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/accounts/signin')
    else:
        return redirect('/')


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = UserDeleteForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user.delete()
            messages.success(request, 'Your Account has been deleted!')
            return redirect('/accounts/signup')
    return render(request, 'errors.html', {'err_code': 405, 'err_type': 'Method Not Allowed'})


@login_required
def deactivate_account(request):
    if request.method == 'POST':
        form = UserDeleteForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user.is_active = False
            request.user.save()
            messages.success(request, 'Your Account has been deactivated! To reactivate, sign in with your username and password.')
            auth.logout(request)
            return redirect('/accounts/signin')
    return render(request, 'errors.html', {'err_code': 405, 'err_type': 'Method Not Allowed'})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, request=request)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile Updated!')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})
