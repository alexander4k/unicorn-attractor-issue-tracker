from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .forms import RegistrationForm, LoginForm
from issues.models import Issue
from .utils import misc
import os

def index(request):
    """
    A view for the homepage, responsible for the login form and 
    data for statistics and summaries
    """
    
    print(os.environ.get("DEVELOPMENT"))
    login_form = LoginForm()

    message = None
    if 'message' in request.session:
        # Load the message to display for successful login, logout or registration
        message = request.session['message']
        del request.session['message']
    
    # Get issues for display in summaries 
    recent_issues = Issue.objects.all().order_by("-updated")
    oldest_issues = Issue.objects.all().order_by("updated")
    most_popular_bugs = Issue.objects.filter(issue_type="BG"
                        ).annotate(number_of_upvotes=Count('upvotes')
                        ).order_by('-number_of_upvotes')
    most_popular_features = Issue.objects.filter(issue_type="FR"
                            ).annotate(number_of_upvotes=Count('upvotes')
                            ).order_by('-number_of_upvotes')
    
    # On the homepage, each summary group displays 6 rows containing an issue
    # If there are less than 6 issues, the rest of the rows are displayed as
    # empty so get the number of empty rows to display
    number_features_to_six = 6 - len(most_popular_features)
    number_bugs_to_six = 6 - len(most_popular_bugs)
    number_recent_to_six = 6 - len(recent_issues)
    number_oldest_to_six = 6 - len(oldest_issues)
    
    # Get dates to filter issues by for statistics
    months = misc.get_previous_dates("-i", "0", 13)
    days = misc.get_previous_dates("0", "-i", 8)
    today = timezone.now()
    
    # Get issues to be displayed in the statistics part of the homepage
    issues_last_twelve_months = misc.get_issues_per_timerange(
                                misc.get_previous_dates("-i", "0", 12)
                                )
    issues_last_seven_days = misc.get_issues_per_timerange(
                                misc.get_previous_dates("0", "-i", 7)
                                )
    issues_today = Issue.objects.filter(
        completed__year=today.year,
        completed__month=today.month,
        completed__day=today.day
        ).count()
    issues_by_status_counts = misc.get_count_of_issues_by_status()
    
    issues_by_status = []
    for count in issues_by_status_counts:
        if count > 0:
            issues_by_status.append(count)
            

    return render(request, 'index.html', 
                {
                    "login_form": login_form,
                    "message":message,
                    "recent_issues":recent_issues,
                    "issues_last_twelve_months":issues_last_twelve_months,
                    "months":months,
                    "issues_last_seven_days":issues_last_seven_days,
                    "days":days,
                    "issues_by_status":issues_by_status,
                    "most_popular_bugs":most_popular_bugs,
                    "most_popular_features":most_popular_features,
                    "oldest_issues":oldest_issues,
                    "number_features_to_six": number_features_to_six,
                    "number_bugs_to_six": number_bugs_to_six,
                    "number_recent_to_six": number_recent_to_six,
                    "number_oldest_to_six": number_oldest_to_six,
                    "range_features_to_six": range(number_features_to_six),
                    "range_bugs_to_six": range(number_bugs_to_six),
                    "range_recent_to_six": range(number_recent_to_six),
                    "range_oldest_to_six": range(number_oldest_to_six),
                    "issues_today": issues_today,
                    "today":today,
                })

def login(request):
    """
    View to log a user in
    Saves message in session for 
    use on the index page upon redirect
    """
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
                
            if login_form.is_valid():
                user = auth.authenticate(
                        username = request.POST["username"],
                        password = request.POST["password"]
                        )
                    
                if user:
                    auth.login(user=user, request=request)
                    request.session['message'] = "You have successfully logged in"
                else:
                    login_form.add_error(None, "Username or password is incorrect")
                    return render(request, 'index.html', {"login_form": login_form})
        else:
            response = render(request, '400.html')
            response.status_code = 400
            return response
    return redirect("index")

def register(request):
    """
    View for registering a user account
    Saves message in session to be used 
    on the index page upon redirect
    """
    if request.user.is_authenticated:
        return redirect("index")
        
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(
                    username = request.POST["username"],
                    password = request.POST["password1"]
                    )
            
            if user:
                auth.login(user=user, request=request)
                request.session['message'] = "You have successfully registered"
                return redirect("index")
            else:
                return redirect("register_error")
        else:
            messages.error(request, "Failed to create account, try again")
    else:         
        registration_form = RegistrationForm()
    return render(request, "register.html", {"registration_form": registration_form})
    
def register_error(request):
    """
    Page to display in case a user cannot register an account
    """
    return render(request, "register_error.html")
    
@login_required
def logout(request):
    """
    View to log a user out
    Stored message in session for use on index page upon redirect
    """
    auth.logout(request)
    request.session['message'] = "You have successfully logged out"
    return redirect("index")
    
