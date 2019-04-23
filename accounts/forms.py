from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    """
    Form used for registering a user modeled after the User model.
    Checks if the supplied email address is taken and if the passwords match.
    """
    email = forms.CharField(label="Email", required=True, widget=forms.EmailInput)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(email=email).exclude(username=username):
            raise ValidationError('Email address must be unique')
        return email
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get("password2")
        
        if not password1 or not password2:
            raise ValidationError("Confirm your password")
            
        if password1 != password2:
            raise ValidationError("Passwords must match")
        return password2
        
class LoginForm(forms.Form):
    """
    Form used to log in a user
    """
    username = forms.CharField(label="Username or email")
    password = forms.CharField(widget=forms.PasswordInput)
        