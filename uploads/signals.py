from .models import Products, UploadFile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

import os


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


@receiver(pre_save, sender=UploadFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    old_release_notes = sender.objects.get(pk=instance.pk).release_notes
    new_release_notes = instance.release_notes

    if old_release_notes and old_release_notes != new_release_notes:
        if os.path.isfile(old_release_notes.path):
            os.remove(old_release_notes.path)