from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator


# Create your models here.
class MailOTP(models.Model):
    email = models.EmailField(validators=[EmailValidator])
    otp_type = models.CharField(max_length=50)
    otp = models.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    date_generated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('email', 'otp_type'), )

    def __str__(self):
        return self.email
