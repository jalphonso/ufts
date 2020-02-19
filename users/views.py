# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from documentation.models import Consent
from .forms import CustomUserCreationForm


def consent(request):
    consent = Consent.objects.all().first()
    if consent:
        context = {'consent': consent.summary}
    else:
        context = {}
    return render(request, 'consent.html', context)


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'