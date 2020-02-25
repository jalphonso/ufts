from django.contrib import admin
from .models import UploadFile, Products


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'products', 'version', 'description', 'md5sum', 'sha256sum', 'uploaded_date',
                    'uploaded_by', 'verified_by', 'verified_date']
    search_fields = ['name', 'file']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            if obj.uploaded_by:
                readonly_fields = readonly_fields + ('uploaded_by',)
            if obj.verified_by:
                readonly_fields = readonly_fields + ('verified_by',)
            if obj.file:
                readonly_fields = readonly_fields + ('file',)
        readonly_fields = readonly_fields + ('md5sum', 'sha256sum')
        return readonly_fields


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['prod_type', 'prod_family', 'prod_model']
    search_fields = ['prod_type', 'prod_family', 'prod_model']
