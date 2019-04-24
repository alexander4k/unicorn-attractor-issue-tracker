from django.test import TestCase
from django.contrib.auth.models import User

from .forms import RegistrationForm

class TestAccountsForms(TestCase):
    def setUp(self):
        User.objects.create(username="test_user", email="test_email@live.com", password="test_password")
        
    def test_registration_form(self):
        data = {
            'username': 'test_user',
            'email': 'test_email@live.com',
            'password1': 'test_password',
            'password2': 'test_passwor',
        }
        form = RegistrationForm(data)
        
        self.assertFalse(form.is_valid())
        
        email_error = form.has_error("email", code="Unique")
        password_match_error = form.has_error("password2", code="Match")

        self.assertTrue(email_error)
        self.assertTrue(password_match_error)
        
        data = {
            'username': 'test_user2',
            'email': 'test_email@hotmail.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        form = RegistrationForm(data)
        
        self.assertTrue(form.is_valid())
        