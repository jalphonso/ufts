from django.contrib import admin
from .models import Misc


@admin.register(Misc)
class MiscAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']