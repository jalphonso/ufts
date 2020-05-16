from datetime import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from .models import UploadFile
from documentation.models import Eula
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain
from users.models import Contract
from ipware import get_client_ip
import logging


logger = logging.getLogger('download_user')


def get_permissions(user):
    now = datetime.now().date()
    groups = user.groups.all()
    download_permissions = []
    for group in groups:
        try:
            contract_obj = Contract.objects.get(name__exact=group)
        except ObjectDoesNotExist:
            continue
        expiry_date = contract_obj.expiry_date
        if expiry_date < now:
            continue
        permissions = list(group.permissions.all())
        for permission in permissions:
            permission_name = permission.codename
            if 'download' in permission_name:
                if permission_name not in download_permissions:
                    download_permissions.append(permission_name)
    return download_permissions


@login_required
@permission_required('uploads.view_uploadfile', raise_exception=True)
def downloads(request):
    download_permissions = get_permissions(request.user)
    dw_client_ip, is_routable = get_client_ip(request)
    upload_list = []
    for permission in download_permissions:
        prod_type = permission.split('_')[0]
        query_set = UploadFile.objects.all().order_by('file').filter(products__prod_type=prod_type)
        upload_list = chain(upload_list, query_set)
    upload_list = list(upload_list)
    context = {
        'uploads': upload_list,
    }
    response = render(request, 'uploads/downloads.html', context)
    return response


@login_required
@permission_required('uploads.view_uploadfile', raise_exception=True)
def download_file(request):
    dw_client_ip, is_routable = get_client_ip(request)
    filename = request.path.split('/')[-1]
    download_permissions = get_permissions(request.user)
    try:
        file_requested = UploadFile.objects.get(file=filename)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, '404.html'))
    is_verified = bool(file_requested.verified_by)
    permission = file_requested.products.prod_type + '_download'

    if is_verified and permission in download_permissions:
        logger.debug('user: {} |ip address: {} |downloaded_file: {}'.format(request.user, dw_client_ip, filename))
        response = HttpResponse()
        response['Content-Type'] = ''
        response['X-Accel-Redirect'] = settings.SOFTWARE_URL + filename
        return response
    else:
        return HttpResponseForbidden(render(request, '403.html'))


@login_required
@permission_required('uploads.view_uploadfile', raise_exception=True)
def download_release_notes(request):
    dw_client_ip, is_routable = get_client_ip(request)
    filename = request.path.split('/')[-1]
    download_permissions = get_permissions(request.user)
    if not filename:
        return HttpResponseNotFound(render(request, '404.html'))
    try:
        associated_software = UploadFile.objects.get(release_notes=filename)
        release_notes = associated_software.release_notes
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, '404.html'))
    is_verified = bool(associated_software.verified_by)
    permission = associated_software.products.prod_type + '_download'
    if is_verified and permission in download_permissions:
        logger.debug('user: {} |ip address: {} |downloaded_file: {}'.format(request.user, dw_client_ip, release_notes))
        response = HttpResponse()
        response['Content-Type'] = ''
        response['X-Accel-Redirect'] = settings.SOFTWARE_URL + 'release_notes/' + release_notes.name
        return response
    else:
        return HttpResponseForbidden(render(request, '403.html'))


@login_required
def eula(request):
    eula = Eula.objects.all().first()
    if eula:
        context = {'eula_summary': eula.summary, 'eula_file': eula.downloadable_file}
    else:
        context = {}
    return render(request, 'uploads/eula.html', context)
