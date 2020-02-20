from django.shortcuts import render
from .models import UploadFile
from documentation.models import Eula
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger('download_user')


@login_required
def downloads(request):
    dw_client_ip = request.META['REMOTE_ADDR']
    upload_list = UploadFile.objects.all().order_by('file')
    filename = ''
    for filename in upload_list:
        print(filename.file)
    context = {
        'uploads': upload_list,
    }
    logger.debug('user: {} |ip address: {} |downloaded_file: {}'.format(request.user, dw_client_ip, filename.file))
    return render(request, 'uploads/downloads.html', context)


@login_required
def eula(request):
    eula = Eula.objects.all().first()
    if eula:
        context = {'eula_summary': eula.summary, 'eula_file': eula.downloadable_file}
    else:
        context = {}
    return render(request, 'uploads/eula.html', context)
