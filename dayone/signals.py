from .models import Book
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

import os


@receiver(post_delete, sender=Book)
def book_delete(sender, instance, **kwargs):
    instance.pdf.delete(False)
    instance.cover.delete(False)


@receiver(pre_save, sender=Book)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).pdf
    except sender.DoesNotExist:
        return False

    new_file = instance.pdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    old_cover = sender.objects.get(pk=instance.pk).cover
    new_cover = instance.cover

    if old_cover and old_cover != new_cover:
        if os.path.isfile(old_cover.path):
            os.remove(old_cover.path)