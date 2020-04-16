from django.contrib import admin
from .models import UploadFile, Products
import logging
from ipware import get_client_ip

logger = logging.getLogger('upload_user')


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
        client_ip, is_forwardable = get_client_ip(request)
        if not change:
            logger.debug('user: {} |ip address: {} |uploaded_file: {}'.format(obj.uploaded_by, client_ip, obj.file))
            if obj.release_notes:
                logger.debug('user: {} |ip address: {} |uploaded_release_notes: {}'.format(obj.uploaded_by, client_ip, obj.release_notes))
        else:
            if 'verified_by' in form.fields:
                logger.debug('user: {} |ip address: {} |verified_file: {}'.format(obj.verified_by, client_ip, obj.file))
                
        super().save_model(request, obj, form, change)
    def delete_model(self, request, obj):
        client_ip, is_forwardable = get_client_ip(request)
        logger.debug('user: {} |ip address: {} |deleted_file: {}'.format(obj.uploaded_by, client_ip, obj.file))
        super().delete_model(request, obj)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['prod_type', 'prod_family', 'prod_model']
    search_fields = ['prod_type', 'prod_family', 'prod_model']
