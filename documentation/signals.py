from .models import Eula, Document
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Eula)
def eula_delete(sender, instance, **kwargs):
    instance.downloadable_file.delete(False)

@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    instance.document.delete(False)
