from .models import Products, UploadFile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_save, sender=Products)
def create_product_permission(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Products)
    permission = Permission.objects.get_or_create(codename=f"{instance.prod_type}_download",
                                           name=f"Can download software for {instance.prod_type}",
                                           content_type=content_type)


@receiver(post_delete, sender=UploadFile)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
    instance.release_notes.delete(False)
