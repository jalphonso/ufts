from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from .models import UploadFile
from documentation.models import Eula
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain
import logging


logger = logging.getLogger('download_user')


@login_required
@permission_required('uploads.view_uploadfile', raise_exception=True)
def downloads(request):
    permissions = request.user.get_all_permissions()
    download_permissions = []
    for permission in permissions:
        if 'download' in permission:
            download_permissions.append(permission.split('_')[0])
    dw_client_ip = request.META['REMOTE_ADDR']
    upload_list = []
    for permission in download_permissions:
        prod_type = permission.split('.')[1]
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
    dw_client_ip = request.META['REMOTE_ADDR']
    filename = request.path.split('/')[-1]
    try:
        file_requested = UploadFile.objects.get(file=filename)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, '404.html'))
    is_verified = bool(file_requested.verified_by)
    permission = 'uploads.' + file_requested.products.prod_type + '_download'
    if is_verified and request.user.has_perm(permission):
        logger.debug('user: {} |ip address: {} |downloaded_file: {}'.format(request.user, dw_client_ip, filename))
        response = HttpResponse()
        response['Content-Type'] = ''
        response['X-Accel-Redirect'] = settings.SOFTWARE_URL + filename
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
