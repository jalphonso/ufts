from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls import reverse

def check_userprofile_middleware(get_response):
    def middleware(request):

        if request.path_info != reverse("profile"):
          if request.user.is_authenticated and not request.user.profile_complete():
              return redirect(reverse("profile"))

        response = get_response(request)

        return response

    return middleware