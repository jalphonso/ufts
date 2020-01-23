from django.db import models


class Jsa(models.Model):
    displayName = models.CharField(max_length=200, blank=True)
    document = models.FileField(upload_to='support/jsas')
    description = models.TextField()

    def __str__(self):
        return self.displayName
