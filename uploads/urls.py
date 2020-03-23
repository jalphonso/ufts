from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.downloads, name='uploads'),
    re_path(r'^file/', views.download_file, name='download_file'),
    path('eula', views.eula, name='eula'),
]
