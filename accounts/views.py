from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

def index(request):
    # View for the homepage
    login_form = LoginForm()
    message = None
    
    if 'message' in request.session:
        # Load the messages to display for successful login, logout and registration
        message = request.session['message']
        del request.session['message']

    return render(request, 'index.html', {"login_form": login_form, "message":message})
    
def login(request):
    # View for login a user in
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
                
            if login_form.is_valid():
                user = auth.authenticate(username = request.POST["username"], password = request.POST["password"])
                    
                if user:
                    auth.login(user=user, request=request)
                    request.session['message'] = "You have successfully logged in"
                else:
                    login_form.add_error(None, "Username or password is incorrect")
                    return render(request, 'index.html', {"login_form": login_form})
            
    return redirect("index")
    
@login_required
def logout(request):
    # View for login a user out
    auth.logout(request)
    request.session['message'] = "You have successfully logged out"
    return redirect("index")
    
def register(request):
    # View for registering a user account
    if request.user.is_authenticated:
        return redirect(reverse("index"))
        
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username = request.POST["username"], password = request.POST["password1"])
            
            if user:
                auth.login(user=user, request=request)
                request.session['message'] = "You have successfully registered"
                return redirect("index")
            else:
                return redirect("register_error")
    else:         
        registration_form = RegistrationForm()
    return render(request, "register.html", {"registration_form": registration_form})
    
def register_error(request):
    # Page to display in case a user cannot register an account
    return render(request, "register_error.html")

    
