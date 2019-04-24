from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Profile

class TestProfilesViews(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        
    def test_get_profile_page(self):
        user = User.objects.get(username="test_user")
        self.client.login(username='test_user', password='test_password')
        
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        
    def test_if_profile_redirects_to_404_if_no_profile(self):
        user = User.objects.get(username="test_user")
        Profile.objects.filter(user=user).delete()
        self.client.login(username='test_user', password='test_password')
        
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        
    def test_if_update_profile_image_redirects_to_404_if_no_profile(self):
        user = User.objects.get(username="test_user")
        Profile.objects.filter(user=user).delete()
        self.client.login(username='test_user', password='test_password')
        
        response = self.client.get(reverse("update_profile_image"))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        
    def test_get_update_profile_image_page(self):
        user = User.objects.get(username="test_user")
        self.client.login(username='test_user', password='test_password')
        
        response = self.client.get(reverse("update_profile_image"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_profile_image.html")
        