from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import LoginForm
from issues.models import Issue

class TestAccountsViews(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        
    def test_get_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
    
    def test_if_login_redirects_to_index_if_user_logged_in(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse("login"), follow=True)
        self.assertRedirects(response, reverse("index"), status_code=302)
        self.assertTemplateUsed(response, "index.html")
        
    def test_if_login_redirects_to_400_page_if_not_post_request(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "400.html")
        
    def test_if_login_redirects_to_index_when_form_invalid(self):
        post_data = {
            "user": "test_user",
            "pass": "test_password"
        }
        response = self.client.post(reverse("login"), post_data, follow=True)
        self.assertRedirects(response, reverse("index"), status_code=302)
        self.assertTemplateUsed(response, "index.html")
        
    def test_if_user_is_authenticated_when_form_is_valid_for_login(self):
        post_data = {
            "username": "test_user",
            "password": "test_password"
        }
        response = self.client.post(reverse("login"), post_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertRedirects(response, reverse("index"), status_code=302)
        self.assertTemplateUsed(response, "index.html")
    
    def test_get_register_page(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
    
    def test_if_register_redirects_to_index_if_user_logged_in(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse("register"), follow=True)
        self.assertRedirects(response, reverse("index"), status_code=302)
        self.assertTemplateUsed(response, "index.html")
        
    def test_if_register_creates_user_if_form_valid_and_redirect_to_index(self):
        post_data = {
            "email": "test_email@live.com",
            "username": "test_user2",
            "password1": "test_password2",
            "password2": "test_password2",
        }
        response = self.client.post(reverse("register"), post_data, follow=True)
        test_user2 = User.objects.get(email="test_email@live.com")
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertEqual("test_user2", test_user2.username)
        self.assertRedirects(response, reverse("index"), status_code=302)
        self.assertTemplateUsed(response, "index.html")
        
    def test_get_register_error_page(self):
        response = self.client.get(reverse("register_error"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register_error.html")
        
    def test_if_logout_logs_user_out_and_redirects(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        authenticated = user.is_authenticated()
        self.assertEqual(True, authenticated)
        response = self.client.get(reverse("logout"), follow=True)
        self.assertFalse(response.context['user'].is_authenticated())
        self.assertRedirects(response, reverse("index"), status_code=302)
        self.assertTemplateUsed(response, "index.html")