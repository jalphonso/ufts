from django.shortcuts import render
from .models import Misc


def misc_list(request):
    files = Misc.objects.all()

    return render(request, 'misc.html', {
        'files': files
    })
