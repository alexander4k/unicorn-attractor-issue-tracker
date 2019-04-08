from django import forms
from django.forms import ModelForm
from .models import Profile

class UpdateImageForm(ModelForm):
    image = forms.ImageField(label="", required=False)
    class Meta:
        model = Profile
        fields = ['image']