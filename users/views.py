# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from documentation.models import Consent
from .forms import CustomUserCreationForm, EditProfileForm


def consent(request):
    consent = Consent.objects.all().first()
    if consent:
        context = {'consent': consent.summary}
    else:
        context = {}
    return render(request, 'consent.html', context)


def edit_profile(request):
    user = request.user
    invalid = False
    submitted_without_change = False
    if request.method == "POST":
        form = EditProfileForm(data=request.POST, instance=user)
        if form.is_valid():
            if form.has_changed():
                user.save()
                return render(request, 'user_profile/profile_changed.html', {'changes': user.diff})
            else:
                submitted_without_change = True
        else:
            invalid = True

    ### Second half of this method handles initial GET requests
    ### or updates page if errors with the submission
    existing_data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'unclas_email': user.unclas_email,
        'class_phone': user.class_phone,
        'unclas_phone': user.unclas_phone,
    }
    ### prepopulate form fields with existing user data
    form = EditProfileForm(initial=existing_data)
    context = {
        'invalid': invalid,
        'no_change': submitted_without_change,
        'form': form,
    }
    return render(request, 'user_profile/edit_profile.html', context)


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
