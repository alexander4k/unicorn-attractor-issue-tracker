from django.conf.urls import url
from django.contrib import admin
from .views import all_issues, bugs, features, create_issue, issue_details, add_upvote, delete_issue

urlpatterns = [
    url(r'^$', all_issues, name="all_issues"),
    url(r'^create_issue/$', create_issue, name="create_issue"),
    url(r'^delete_issue(?P<id>\d+)/$', delete_issue, name="delete_issue"),
    url(r'^issue_details(?P<id>\d+)/$', issue_details, name="issue_details"),
    url(r'^add_upvote(?P<id>\d+)/$', add_upvote, name="add_upvote"),
    
    url(r'^popular_sort/$', all_issues, {'sort_type': 'popular'}, name='issues_by_popular'),
    url(r'^popular_sort/(?P<page>\d+)/$', all_issues, {'sort_type': 'popular'}, name='issues_by_popular_paged'),
    url(r'^comments_sort/$', all_issues, {'sort_type': 'comments'}, name='issues_by_comments'),
    url(r'^comments_sort/(?P<page>\d+)/$', all_issues, {'sort_type': 'comments'}, name='issues_by_comments_paged'),
    
    url(r'^bugs/$', bugs, name="bugs"),
    url(r'^bugs/popular_sort/$', bugs, {'sort_type': 'popular'}, name='bugs_by_popular'),
    url(r'^bugs/popular_sort/(?P<page>\d+)/$', bugs, {'sort_type': 'popular'}, name='bugs_by_popular_paged'),
    url(r'^bugs/comments_sort/$', bugs, {'sort_type': 'comments'}, name='bugs_by_comments'),
    url(r'^bugs/comments_sort/(?P<page>\d+)/$', bugs, {'sort_type': 'comments'}, name='bugs_by_comments_paged'),
    
    url(r'^features/$', features, name="features"),
    url(r'^features/popular_sort/$', features, {'sort_type': 'popular'}, name='features_by_popular'),
    url(r'^features/popular_sort/(?P<page>\d+)/$', features, {'sort_type': 'popular'}, name='features_by_popular_paged'),
    url(r'^features/comments_sort/$', features, {'sort_type': 'comments'}, name='features_by_comments'),
    url(r'^features/comments_sort/(?P<page>\d+)/$', features, {'sort_type': 'comments'}, name='features_by_comments_paged'),
]
