from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Products(models.Model):
    prod_type = models.CharField(max_length=100, default='')  # Routing, Switching, Security, SDN, Packet Optical
    prod_family = models.CharField(max_length=100, default='')  # Product Family
    prod_model = models.CharField(max_length=100, default='')  # MX5, MX10, MX40

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.prod_model


class Document(models.Model):
    name = models.CharField(max_length=100, default='', editable=True)
    category = models.CharField(max_length=100, default='')  # data sheet, release notes
    document = models.FileField(upload_to='support/documentation',)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Eula(models.Model):
    name = models.CharField(max_length=100, default='', editable=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    downloadable_file = models.FileField(upload_to='support/documentation',)


    def __str__(self):
        return self.name

class Consent(models.Model):
    name = models.CharField(max_length=100, default='', editable=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name


@receiver(post_delete, sender=Eula)
def eula_delete(sender, instance, **kwargs):
    instance.downloadable_file.delete(False)

@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    instance.document.delete(False)
