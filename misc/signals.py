from .models import Misc
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Misc)
def misc_delete(sender, instance, **kwargs):
    instance.file.delete(False)
