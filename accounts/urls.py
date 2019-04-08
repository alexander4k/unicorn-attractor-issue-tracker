from django.conf.urls import url, include
from .views import *
from profiles import urls as urls_profiles
urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^register_error/$', register_error, name='register_error'),
    url(r'^logout/$', logout, name="logout"),
    url(r'^login/$', login, name="login"),
    url(r'^profile/', include(urls_profiles)),
]