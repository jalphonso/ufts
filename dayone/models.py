from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdf/')
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Book)
def book_delete(sender, instance, **kwargs):
    instance.pdf.delete(False)
    instance.cover.delete(False)
