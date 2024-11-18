from django import forms
from .models import Client



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['code_client', 'nom', 'adresse', 'email', 'telephone']
