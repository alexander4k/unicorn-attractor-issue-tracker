from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Issue, Upvote, Comment
from .forms import IssueForm, CommentForm
from .utils import misc

def all_issues(request, sort_type=None):
    """
    View used to display all existing issues
    """
    issues_list = misc.filter_and_sort_issues('.+', sort_type)
    issues = misc.pagination(issues_list, request.GET.get('page', 1))
    return render(request, 'all_issues.html',
        {
            "issues": issues,
            "issues_list":issues_list
        })
    
def bugs(request, sort_type=None):
    """
    View used to display all existing bugs
    """
    issues_list = misc.filter_and_sort_issues("BG", sort_type)
    issues = misc.pagination(issues_list, request.GET.get('page', 1))
    return render(request, 'bugs.html', 
        {
            "issues": issues,
            "issues_list":issues_list
        })
    
def features(request, sort_type=None):
    """
    View used to display all existing feature requests
    """
    issues_list = misc.filter_and_sort_issues("FR", sort_type)
    issues = misc.pagination(issues_list, request.GET.get('page', 1))
    return render(request, 'features.html', 
        {
            "issues": issues, "issues_list":issues_list
        })
    
@login_required
def create_issue(request):
    """
    View used to create an issue
    """
    if not hasattr(request.user, 'profile'):
        # Only allow a user with a profile to create an issue
        response = render(request, '403.html')
        response.status_code = 403
        return response
        
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
            return redirect("create_issue")
    else:
        form = IssueForm()
    return render(request, "create_issue.html", {'form': form})

@login_required
def delete_issue(request, id):
    """
    View used to delete an issue
    """
    issue = get_object_or_404(Issue, pk=id)
    if issue.author == request.user:
        issue.delete()
    return redirect('all_issues')
    
def issue_details(request, id):
    """
    View used to display the details of an issue
    along with providing commenting functionality
    """
    message = None
    if 'message' in request.session:
        # Load the messages to display for no upvotes to 
        # spend or a bug already having been upvoted
        message = request.session['message']
        del request.session['message']
        
    issue = get_object_or_404(Issue, pk=id)
    comments_list = Comment.objects.filter(related_issue=issue
                    ).order_by('-date_created')
    comments = misc.pagination(comments_list, request.GET.get('page', 1))
    
    upvoting_disabled = False
    
    if request.user.is_authenticated:
        upvote = Upvote.objects.filter(related_issue=id, author=request.user)
        if upvote and issue.issue_type == "BG":
            # Check if user has already upvoted a bug and
            # if yes, disable further ability to upvote
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
            issue.updated = timezone.now()
            issue.save()
            return redirect("issue_details", id)
        else:
            response = render(request, '500.html')
            response.status_code = 500
            return response
    else:         
        comment_form = CommentForm()
        
    return render(request, 'issue_details.html', {
        "issue": issue,
        "comments": comments,
        "comments_list": comments_list,
        "comment_form": comment_form,
        "upvoting_disabled": upvoting_disabled,
        "message": message,
    })

@login_required    
def add_upvote(request, id):
    """
    View responsible for adding an upvote to an issue
    Only logged in users that have a profile can upvote an issue
    """
    if not hasattr(request.user, 'profile') or request.user.is_anonymous():
        # If user is not logged in or has no profile, send to error page
        response = render(request, '403.html')
        response.status_code = 403
        return response
    else:
        upvotes_remaining = request.user.profile.upvotes_owned 
    
    issue = get_object_or_404(Issue, pk=id)

    if issue.issue_type == "BG":
        if not Upvote.objects.filter(related_issue=id, author=request.user):
            # For bugs, if a user hasn't already upvoted an issue,
            # create an upvote otherwise send back to issue details
            # with an error message 
            Upvote.objects.create(
                author = request.user,
                related_issue = issue
                )
            return redirect('issue_details', id)
        else:
            request.session['message'] = "You already upvoted this issue"
    elif issue.issue_type == "FR":
        if upvotes_remaining != 0:
            # For feature requests, as long as a user has more than 0 upvotes
            # they can keep upvoting the feature request
            Upvote.objects.create(
                author = request.user,
                related_issue = issue
                )
            request.user.profile.upvotes_owned -= 1
            request.user.profile.save()
            return redirect('issue_details', id)
        else:
            request.session['message'] = "You don't have upvotes to spend"
        
    return redirect("issue_details", id)
        
    