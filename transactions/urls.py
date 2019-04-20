from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^begin_purchase/$', begin_purchase, name="begin_purchase"),
    url(r'^continue_purchase/$', continue_purchase, name="continue_purchase"),
    url(r'^finish_purchase/$', finish_purchase, name="finish_purchase"),
]
    