from django.db import models


class History(models.Model):
    text = models.TextField(default='', editable=True)

    def __str__(self):
        return self.text