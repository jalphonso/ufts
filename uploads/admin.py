from django.contrib import admin
from .models import UploadFile, Products


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'products', 'version', 'description', 'md5sum', 'sha256sum', 'uploaded_date',
                    'uploaded_by', 'verified_by', 'verified_date']
    search_fields = ['name', 'file']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['prod_type', 'prod_family', 'prod_model']
    search_fields = ['prod_type', 'prod_family', 'prod_model']
