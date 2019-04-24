from django.test import TestCase
from django.contrib.auth.models import User

class TestProfileModels(TestCase):
    def setUp(self):
        User.objects.create(username="test_user", password="test_password")
        
    def test_profile_str_method(self):
        test_user = User.objects.get(username="test_user")
        profile = test_user.profile

        self.assertEqual('Profile of %s' % (test_user.username), str(profile))

        
    
        
    