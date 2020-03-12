from .models import Book
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Book)
def book_delete(sender, instance, **kwargs):
    instance.pdf.delete(False)
    instance.cover.delete(False)
