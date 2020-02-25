from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Jsa(models.Model):
    displayName = models.CharField(max_length=200, blank=True)
    document = models.FileField(upload_to='support/jsas')
    description = models.TextField()

    def __str__(self):
        return self.displayName


@receiver(post_delete, sender=Jsa)
def jsa_delete(sender, instance, **kwargs):
    instance.document.delete(False)
