from random import randint
from django.conf import settings
from django.core.mail import send_mail
from users.context_processors import otp_type_task_mapping, global_variables

def generate_otp():
    return randint(100000, 999999)

def send_otp(request, email, otp_type, otp):
    mysite = global_variables(request)['mysite']

    message = f'''<!doctype html>
                <html lang="en">
                    <head></head>
                    <body>
                        Hello There,<br/><br/>
                        Welcome to {mysite}. Your OTP to {otp_type_task_mapping[otp_type]} is <strong>{otp}</strong>.<br/><br/>
                        Thanks,<br/>
                        {mysite} Team.
                    </body>
                </html>'''

    send_mail(
        f'[ {mysite} ] - OTP Request',
        otp,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=message
    )