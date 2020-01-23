from django.db import models
from django.conf import settings


class Message(models.Model):
    heading = models.CharField(max_length=25)
    message = models.TextField()
    date_added = models.DateField(auto_now_add=True, editable=False)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_creator', on_delete=models.CASCADE)
    pinned = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.heading
