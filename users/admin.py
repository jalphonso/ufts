# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Contract


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'unclas_email', 'class_phone', 'unclas_phone',
                    'subscribe_to_emails', 'company']


UserAdmin.fieldsets += ('Profile', {'fields': ('unclas_email', 'class_phone', 'unclas_phone',
                        'subscribe_to_emails', 'company')}),
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['name', 'expiry_date']