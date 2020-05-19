from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from .models import UploadFile, Products
import logging
from ipware import get_client_ip

logger = logging.getLogger('upload_user')


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'products', 'version', 'description', 'md5sum', 'sha256sum', 'uploaded_date',
                    'uploaded_by', 'verified_by', 'verified_date']
    search_fields = ['name', 'file']
    actions = ['verify_files']
    change_form_template = "upload_changeform.html"

    def response_change(self, request, obj):
        client_ip, is_routable = get_client_ip(request)
        if "_verify" in request.POST:
            if not obj.verified_by and obj.uploaded_by != request.user:
                obj.verified_by=request.user
                obj.save()
                messages.add_message(request,messages.SUCCESS, f'File verified by {request.user}.')
                logger.debug(f'user: {obj.verified_by} |ip address: {client_ip} |verified_file: {obj.file}')
            else:
                if obj.verified_by:
                    messages.add_message(request,messages.ERROR, 'File is already verified.')
                else:
                    messages.add_message(request,messages.ERROR,
                                         f'File cannot be verified by {request.user} as you are the uploader.')

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def verify_files(self, request, queryset):
        client_ip, is_routable = get_client_ip(request)
        notuploader=queryset.filter(~Q(uploaded_by = request.user))
        validateable=notuploader.filter(verified_by__isnull = True)
        if validateable.count() == 0:
            messages.add_message(request,messages.ERROR,
                                 f'None of the selected files can be verified by {request.user}. '
                                 f'Either files were already verified, or they were uploaded by {request.user}')
        elif validateable.count() != queryset.count():
            messages.add_message(request,messages.WARNING,
                                 f'{validateable.count()} file(s) verified. '
                                 f'{queryset.count()-validateable.count()} cannot be verified by {request.user}. '
                                 f'Either files were already verified, or they were uploaded by {request.user}')
            for validated in validateable:
                logger.debug(f'user: {validated.verified_by} |ip address: {client_ip} |verified_file: {validated.file}')
            validateable.update(verified_by=request.user)
        else:
            messages.add_message(request, messages.SUCCESS, f'{validateable.count()} file(s) have been verified')
            for validated in validateable:
                logger.debug(f'user: {validated.verified_by} |ip address: {client_ip} |verified_file: {validated.file}')
            validateable.update(verified_by=request.user)
    verify_files.short_description = "Verify selected uploaded files"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        readonly_fields = readonly_fields + ('uploaded_by','verified_by')
        if obj:
            if obj.file:
                readonly_fields = readonly_fields + ('file',)
        readonly_fields = readonly_fields + ('md5sum', 'sha256sum')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        client_ip, is_routable = get_client_ip(request)
        if not change:
            obj.uploaded_by = request.user
            fixed_name=obj.file.name.replace(' ','_')
            if obj.release_notes:
                fixed_relnotes=obj.release_notes.name.replace(' ','_')
                logger.debug(f'user: {obj.uploaded_by} |ip address: {client_ip} |uploaded_file: {fixed_name} '
                             f'|uploaded_release_notes: {fixed_relnotes}')
            else:
                logger.debug(f'user: {obj.uploaded_by} |ip address: {client_ip} |uploaded_file: {fixed_name}')
        else:
            if 'release_notes' in form.changed_data:
                fixed_relnotes=obj.release_notes.name.replace(' ','_')
                logger.debug(f'user: {request.user} |ip address: {client_ip} |uploaded_release_notes: {fixed_relnotes}')
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        client_ip, is_routable = get_client_ip(request)
        logger.debug(f'user: {obj.uploaded_by} |ip address: {client_ip} |deleted_file: {obj.file}')
        super().delete_model(request, obj)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['prod_type', 'prod_family', 'prod_model']
    search_fields = ['prod_type', 'prod_family', 'prod_model']
