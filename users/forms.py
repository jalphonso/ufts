# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'company', 'contract_number')


class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "here: <a href=\"../password/\">RESET PASSWORD</a>."))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'company', 'contract_number')
