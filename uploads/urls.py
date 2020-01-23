from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloads, name='uploads'),
    path('upload_software', views.upload_software, name='upload_software'),
    path('verify_software', views.verify_software, name='verify_software'),
]
