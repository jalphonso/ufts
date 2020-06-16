from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
import hashlib

fs_software = FileSystemStorage(location=settings.SOFTWARE_ROOT, base_url=settings.SOFTWARE_URL)
fs_release_notes = FileSystemStorage(location=settings.SOFTWARE_ROOT + 'release_notes/', base_url=settings.SOFTWARE_URL + 'release_notes/')

class Products(models.Model):
    prod_type = models.CharField(max_length=100, default='')  # Routing, Switching, Security, SDN, Packet Optical
    prod_family = models.CharField(max_length=100, default='')  # Product Family
    prod_model = models.CharField(max_length=100, default='')  # MX5, MX10, MX40

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.prod_model


class UploadFile(models.Model):
    name = models.CharField(max_length=200, blank=True, editable=True)
    file = models.FileField(storage=fs_software)
    release_notes = models.FileField(storage=fs_release_notes, blank=True, null=True)
    version = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=200)
    md5sum = models.CharField(max_length=32, help_text='128bit, 32 Characters', blank=True, editable=True)
    sha256sum = models.CharField(max_length=64, help_text='256bit, 64 Characters', blank=True, editable=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='uploader')
    uploaded_date = models.DateField(auto_now_add=True, editable=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='verifier')
    verified_date = models.DateField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):

    #     # with self.file.open('rb') as f:
    #     #     hash256 = hashlib.sha256()
    #     #     md5hash = hashlib.md5()
    #     #     for chunk in f.chunks():
    #     #         hash256.update(chunk)
    #     #         md5hash.update(chunk)
    #     #     self.sha256sum = hash256.hexdigest()
    #     #     self.md5sum = md5hash.hexdigest()
    #     self.filesize = self.file.size
    #     super(UploadFile, self).save(*args, **kwargs)