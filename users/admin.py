# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'unclas_email', 'class_phone', 'unclas_phone', 'jsa', 'company', 'contract_number']


UserAdmin.fieldsets += ('Profile', {'fields': ('unclas_email', 'class_phone', 'unclas_phone', 'jsa', 'company', 'contract_number')}),
admin.site.register(CustomUser, CustomUserAdmin)
