from django import forms
from .models import UploadFile


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('name', 'file', 'version', 'description', 'md5sum', 'sha256sum', 'uploaded_by')
