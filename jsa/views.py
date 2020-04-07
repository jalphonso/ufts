from django.shortcuts import render
from .models import Jsa
from django.contrib.auth.decorators import login_required
from lib.utilities import do_user_logging


def index(request):
    jsa_list = Jsa.objects.all().order_by('date')

    context = {'documents': jsa_list}
    do_user_logging(request)
    return render(request, 'jsa/index.html', context)
