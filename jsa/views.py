from django.shortcuts import render
from .models import Jsa
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lib.utilities import do_user_logging


@login_required
def index(request):
    jsa_list = Jsa.objects.all().order_by('document')
    page = request.GET.get('page', 1)
    paginator = Paginator(jsa_list, 10)
    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {'documents': documents}
    do_user_logging(request)
    return render(request, 'jsa/index.html', context)
