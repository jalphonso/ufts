from datetime import date
from django.core.exceptions import ValidationError
from django.db import models


class Jsa(models.Model):
    displayName = models.CharField(max_length=200, blank=True)
    document = models.FileField(upload_to='support/jsas')
    description = models.TextField()
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.displayName

    def clean(self):
        if self.date > date.today():
            raise ValidationError("The date cannot be in the future!")