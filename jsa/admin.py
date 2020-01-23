from django.contrib import admin
from .models import Jsa


@admin.register(Jsa)
class JsaAdmin(admin.ModelAdmin):
    list_display = ['displayName', 'document', 'description']