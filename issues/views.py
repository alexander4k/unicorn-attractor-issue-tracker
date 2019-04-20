from django.shortcuts import render, redirect, reverse
from .models import Issue, Upvote, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import IssueForm, CommentForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import *

from .utils import misc


# Create your views here.
def all_issues(request, sort_type=None):
    issues_list = misc.filter_and_sort_issues('.+', sort_type)
    issues = misc.pagination(issues_list, request.GET.get('page', 1))
    return render(request, 'all_issues.html', {"issues": issues})
    
def bugs(request, sort_type=None):
    issues_list = misc.filter_and_sort_issues("BG", sort_type)
    issues = misc.pagination(issues_list, request.GET.get('page', 1))
    return render(request, 'bugs.html', {"issues": issues})
    
def features(request, sort_type=None):
    issues_list = misc.filter_and_sort_issues("FR", sort_type)
    issues = misc.pagination(issues_list, request.GET.get('page', 1))
    return render(request, 'features.html', {"issues": issues})
    
@login_required
def create_issue(request):
    if not hasattr(request.user, 'profile'):
        response = render(request, '403.html')
        response.status_code = 403
        
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            
            issue_data = form.cleaned_data
            new_issue = Issue.objects.create(
                title = issue_data['title'],
                author = request.user,
                issue_type = issue_data['issue_type'],
                description = issue_data['description']
            )
            return redirect('issue_details', id=new_issue.id)
        else:
            messages.error(request, "Failed to create issue, try again")
    else:
        form = IssueForm()
    return render(request, "create_issue.html", {'form': form})

@login_required
def delete_issue(request, id):
    issue = get_object_or_404(Issue, pk=id)
    if issue.author == request.user:
        issue.delete()
    return redirect('all_issues')
    
def issue_details(request, id):
    issue = get_object_or_404(Issue, pk=id)
    comments_list = Comment.objects.filter(related_issue=issue).order_by('-date_created')
        
    comments = misc.pagination(comments_list, request.GET.get('page', 1))
    
    upvoting_disabled = False
    
    if request.user.is_authenticated:
        upvote = Upvote.objects.filter(related_issue=id, author=request.user)
        if upvote and issue.issue_type == "BG":
            upvoting_disabled = True
    else:
        upvoting_disabled = True
            
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_data = comment_form.cleaned_data
            new_comment = Comment.objects.create(
                author = request.user,
                related_issue = issue,
                content = comment_data["content"]
            )
            issue.updated = datetime.now()
            issue.save()
            return redirect("issue_details", id)
        else:
            messages.error(request, "Failed to add comment, try again")
    else:         
        comment_form = CommentForm()
    return render(request, 'issue_details.html', {"issue": issue, "comments": comments, "comment_form": comment_form, "upvoting_disabled": upvoting_disabled})

@login_required    
def add_upvote(request, id):
    if not hasattr(request.user, 'profile') or not request.user.is_authenticated():
        response = render(request, '403.html')
        response.status_code = 403
    else:
        upvotes_remaining = request.user.profile.upvotes_owned 
    
    issue = get_object_or_404(Issue, pk=id)
    
    if issue.issue_type == "BG":
        if not Upvote.objects.filter(related_issue=id, author=request.user):
            Upvote.objects.create(
                author = request.user,
                related_issue = issue
                )
            return redirect('issue_details', id=issue.id)
        else:
            upvoted = True
            messages.error(request, "You've already upvoted the issue")
    else:
        if upvotes_remaining != 0:
            Upvote.objects.create(
                author = request.user,
                related_issue = issue
                )
            request.user.profile.upvotes_owned -= 1
            request.user.profile.save()
            return redirect('issue_details', id=issue.id)
        else:
            messages.error(request, "You don't have upvotes to spend")
        
    return render(request, "issue_details.html", {"issue": issue, "comments": comments, "comment_form": comment_form})
        
    