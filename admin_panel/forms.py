from django import forms
from .models import IPO

class IPOForm(forms.ModelForm):
    class Meta:
        model = IPO
        fields = '__all__'