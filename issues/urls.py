from django.conf.urls import url
from django.contrib import admin
from .views import issues, create_issue, issue_details, add_upvote

urlpatterns = [
    url(r'^all_issues/$', issues, name="issues"),
    url(r'^create_issue/$', create_issue, name="create_issue"),
    url(r'^issue_details(?P<id>\d+)/$', issue_details, name="issue_details"),
    url(r'^add_upvote(?P<id>\d+)/$', add_upvote, name="add_upvote"),
]
