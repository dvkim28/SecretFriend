from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from config import settings
from django.utils.timezone import now


class User(AbstractUser):
    country = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'email verification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:EmailVerificationView', kwargs={'email':self.user.email, 'code':self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Verification for {self.user.email}'
        message = f'Verification for {self.user.email} go to the verification link {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


class Wish(models.Model):
    name = models.CharField(max_length= 128)
    url = models.CharField(max_length= 128)
    comment = models.TextField()
    parent = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
