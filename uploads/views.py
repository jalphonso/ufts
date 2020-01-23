from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import SoftwareForm
from .models import UploadFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from .forms import SoftwareForm
logger = logging.getLogger('download_user')
uploads = logging.getLogger('upload_user')
verify = logging.getLogger('verify_user')


@login_required
def downloads(request):
    dw_client_ip = request.META['REMOTE_ADDR']
    upload_list = UploadFile.objects.all().order_by('file')
    filename = ''
    for filename in upload_list:
        print(filename.file)

    page = request.GET.get('page', 1)
    paginator = Paginator(upload_list, 20)
    try:
        uploads = paginator.page(page)
    except PageNotAnInteger:
        uploads = paginator.page(1)
    except EmptyPage:
        uploads = paginator.page(paginator.num_pages)
    context = {
        'uploads': uploads,
    }
    logger.debug('user: {} |ip address: {} |downloaded_file: {}'.format(request.user, dw_client_ip, filename.file))
    return render(request, 'uploads/downloads.html', context)


@login_required
def upload_software(request):
    up_client_ip = request.META['REMOTE_ADDR']
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)

        context['url'] = fs.url(name)
    logger.debug('user: {} |ip address: {} |uploaded_file: {}'.format(request.user, up_client_ip, filename.file))
    return render(request, 'uploads/upload_software.html', context)


@login_required
def verify_software(request):
    client_ip = request.META['REMOTE_ADDR']
    upload_list = UploadFile.objects.all().order_by('file')
    filename = ''
    for filename in upload_list:
        print(filename.file)

    page = request.GET.get('page', 1)
    paginator = Paginator(upload_list, 20)
    try:
        uploads = paginator.page(page)
    except PageNotAnInteger:
        uploads = paginator.page(1)
    except EmptyPage:
        uploads = paginator.page(paginator.num_pages)
    context = {
        'uploads': uploads,
    }
    uploads.debug('user: {} |ip address: {} |verified_file: {}'.format(request.user, client_ip, filename.file))
    return render(request, 'uploads/verify_software.html', context)

