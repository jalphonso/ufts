from django.contrib import admin
from .models import Document, Products


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'document', 'description', 'product']


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['prod_type', 'prod_family', 'prod_model']
