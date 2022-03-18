from django.contrib import messages
from django.shortcuts import HttpResponse
from django.views.generic import View
from django.utils.safestring import mark_safe
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
                otp = None
            else:
                form.instance.otp = otp
                form.instance.otp_type = otp_type
                form.save()
        return HttpResponse(str(otp))
