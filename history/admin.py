from django.contrib import admin
from .models import History


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['text']