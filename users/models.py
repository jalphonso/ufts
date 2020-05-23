# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from lib.mixins import ModelDiffMixin


class CustomUser(AbstractUser, ModelDiffMixin):
    first_name = models.CharField(max_length=50, default='', editable=True)
    last_name = models.CharField(max_length=50, default='', editable=True)
    email = models.EmailField(max_length=100, default='', editable=True)
    unclas_email = models.EmailField(max_length=100, default='', editable=True)
    class_phone = models.CharField(max_length=30, default='', editable=True)
    unclas_phone = models.CharField(max_length=30, default='', editable=True)
    company = models.CharField(max_length=50, default='', editable=True)
    subscribe_to_emails = models.BooleanField(default=True, editable=True)


    def __str__(self):
        return self.username

    def profile_complete(self):
        return bool(self.first_name and self.last_name and self.email and self.unclas_email
                    and self.class_phone and self.unclas_phone and self.company)


class Contract(models.Model):
    name = models.CharField(max_length=50, default='', editable=True)
    expiry_date = models.DateField(editable=True)
