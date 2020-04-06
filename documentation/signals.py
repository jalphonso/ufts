from .models import Eula, Document
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

import os


@receiver(post_delete, sender=Eula)
def eula_delete(sender, instance, **kwargs):
    instance.downloadable_file.delete(False)


@receiver(pre_save, sender=Eula)
def auto_delete_eula_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).downloadable_file
    except sender.DoesNotExist:
        return False

    new_file = instance.downloadable_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    instance.document.delete(False)


@receiver(pre_save, sender=Document)
def auto_delete_document_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).document
    except sender.DoesNotExist:
        return False

    new_file = instance.document
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
