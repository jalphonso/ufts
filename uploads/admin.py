from django.contrib import admin
from .models import UploadFile, Products
import logging

logger = logging.getLogger('upload_user')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'products', 'version', 'description', 'md5sum', 'sha256sum', 'uploaded_date',
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
        else:
            readonly_fields = readonly_fields + ('verified_by',)
        readonly_fields = readonly_fields + ('md5sum', 'sha256sum')
        return readonly_fields
    def save_model(self, request, obj, form, change):
        client_ip = get_client_ip(request)
        logger.debug('user: {} |ip address: {} |downloaded_file: {}'.format(obj.uploaded_by, client_ip, obj.file))
        super().save_model(request, obj, form, change)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['prod_type', 'prod_family', 'prod_model']
    search_fields = ['prod_type', 'prod_family', 'prod_model']
