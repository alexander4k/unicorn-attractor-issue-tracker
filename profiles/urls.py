from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', profile, name="profile"),
    url(r'^update_profile_image/$', update_profile_image , name="update_profile_image"),
]