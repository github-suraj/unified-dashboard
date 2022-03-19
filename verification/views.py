import json
from django.shortcuts import HttpResponse
from django.views.generic import View
from . import utils
from .forms import MailOTPForm
from .models import MailOTP

# Create your views here.
class MailOPTCreateView(View):
    form_class = MailOTPForm

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        otp_type = kwargs.get('otp_type')

        mail_otp = MailOTP.objects.filter(email=email, otp_type=otp_type)
        mail_otp.delete()

        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                otp = utils.generate_otp()
                utils.send_otp(request, email, otp_type, str(otp))
            except Exception as err:
                output = {
                    'success': False,
                    'message': '''We are facing some issue in sending email with OTP, Please try again in sometime.<br/>
                        Please make sure you\'re internet connection is stable.'''
                }
            else:
                form.instance.otp = otp
                form.instance.otp_type = otp_type
                form.save()
                output = {
                    'success': True,
                    'message': '''We have emailed you an OPT for creating account.<br/>
                        If an account exists with the email you entered. You should receive them shortly.<br/>
                        If you don\'t receive an email in inbox, please check your spam folder.'''
                }
        else:
            output = {
                'success': False,
                'message': 'You have entered an Invalid email address'
            }
        return HttpResponse(json.dumps(output))
