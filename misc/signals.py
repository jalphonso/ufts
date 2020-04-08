from .models import Misc
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

import os


@receiver(post_delete, sender=Misc)
def misc_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(pre_save, sender=Misc)
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