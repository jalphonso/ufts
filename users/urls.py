# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.edit_profile, name='profile'),
    path('', views.consent, name='consent'),

]