from django.shortcuts import render
from .models import Jsa


def index(request):
    jsa_list = Jsa.objects.all().order_by('date')

    context = {'documents': jsa_list}
    return render(request, 'jsa/index.html', context)
