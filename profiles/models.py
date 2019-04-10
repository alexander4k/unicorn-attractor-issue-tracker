from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import os

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/profile_images", null=True, blank=True)
    upvotes_owned = models.IntegerField(default=0)
    
    def __str__(self):
        return 'Profile of %s' % (self.user.username)
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Every time a user registers an account, create that user's profile
    if created:
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    # Delete old image when updating profile image
    if not instance.pk:
        return False
        
    if not Profile.objects.get(pk=instance.pk).image:
        return False
    else:
        old_file = Profile.objects.get(pk=instance.pk).image
        new_file = instance.image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)