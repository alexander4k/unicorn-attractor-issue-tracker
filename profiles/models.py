from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import os

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', blank=True)
    upvotes_owned = models.IntegerField(default=5)
    
    def __str__(self):
        return 'Profile of %s' % (self.user.username)
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    If a user account is registered, create a corresponding user profile
    """
    if created:
        Profile.objects.create(user=instance)
                
