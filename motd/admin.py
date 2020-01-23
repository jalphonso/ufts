from django.contrib import admin
from .models import Message


@admin.register(Message)
class MotdAdmin(admin.ModelAdmin):
    list_display = ['heading', 'message', 'date_added', 'create_user', 'pinned', 'send_email']
