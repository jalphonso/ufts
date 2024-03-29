from django.shortcuts import render
from .models import Document
from django.contrib.auth.decorators import login_required
import logging
from ipware import get_client_ip

logger = logging.getLogger('documentation_user')


def index(request):
    client_ip, is_routable = get_client_ip(request)
    document_list = Document.objects.all().order_by('document')
    for filename in document_list:
        print(filename.document)

    filelist = []  # myfile is the key of a multi value dictionary, values are the uploaded files
    for f in request.FILES.getlist('upload_list.file'):  # myfile is the name of your html file button
        filename = f.name
        filelist.append(filename)
        logger.debug('user: {} |ip address: {} |viewed documentation: {}'.format(request.user, client_ip, filename.document))

    context = {'documents': document_list}
    return render(request, 'documentation/index.html', context)