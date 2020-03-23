from .models import Jsa
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Jsa)
def jsa_delete(sender, instance, **kwargs):
    instance.document.delete(False)
