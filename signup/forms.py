from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Document


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class UploadFileForm(forms.ModelForm):
    file=forms.FileField(label="Upload File")
    class Meta:
        model = Document
        fields = ['file']


class DecryptForm(forms.Form):
    image=forms.ImageField(label="Insert Image Password")



