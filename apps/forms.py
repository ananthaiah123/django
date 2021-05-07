from django import forms
 
from .models import Audio1doc
 
class Audio1Form(forms.ModelForm):
 
    class Meta:
        model = Audio1doc
        fields = ['Name', 'Action']