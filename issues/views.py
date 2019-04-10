from django.shortcuts import render, redirect
from .models import Issue, Upvote, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import IssueForm, CommentForm
from django.contrib.auth.models import User
from datetime import *


# Create your views here.
def issues(request):
    issues = Issue.objects.all()
    return render(request, 'issues.html', {"issues":issues})
    
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
    
def issue_details(request, id):
    issue = Issue.objects.get(pk=id)
    comments = Comment.objects.filter(related_issue=issue)
    upvoted = False
    
    if request.user.is_authenticated:
        if Upvote.objects.filter(related_issue=id, author=request.user) and issue.issue_type == "BG":
            upvoted = True
    else:
        upvoted = True
            
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        print(comment_form["content"])
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
    return render(request, 'issue_details.html', {"issue": issue, "comments": comments, "comment_form": comment_form, "upvoted": upvoted})

@login_required    
def add_upvote(request, id):
    if not hasattr(request.user, 'profile') or not request.user.is_authenticated():
        response = render(request, '403.html')
        response.status_code = 403
    else:
        upvotes_remaining = request.user.profile.upvotes_owned 

    issue = Issue.objects.get(pk=id)
    comments = Comment.objects.filter(related_issue=issue)
    comment_form = CommentForm()
    
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
        
    