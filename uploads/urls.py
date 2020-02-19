from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloads, name='uploads'),
    path('eula', views.eula, name='eula'),
]
