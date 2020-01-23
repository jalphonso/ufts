# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    unclas_email = models.CharField(max_length=50, default='', editable=True)
    class_phone = models.CharField(max_length=30, default='', editable=True)
    unclas_phone = models.CharField(max_length=30, default='', editable=True)
    company = models.CharField(max_length=30, default='', editable=True)
    contract_number = models.CharField(max_length=30, default='', editable=True, blank=True, null=True)
    jsa = models.BooleanField(default=True, editable=True, blank=True, null=True)


    def __str__(self):
        return self.email