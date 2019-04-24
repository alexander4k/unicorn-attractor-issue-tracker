from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import UpdateImageForm

   
def profile(request):
    """
    View to display a user's profile
    If a user has no profile, sends the user to the 404 page
    """
    if not hasattr(request.user, 'profile'):
        raise Http404 
    else:
        profile = request.user.profile 

    return render(request, 'profile.html', {'profile': profile})

@login_required
def update_profile_image(request):
    """
    View to update a user's profile image
    If a user has no profile, sends the user to the 404 page
    """
    if not hasattr(request.user, 'profile'):
        raise Http404 
    else:
        profile = request.user.profile 
        
    if request.method == "POST":
        form = UpdateImageForm(request.FILES)
        
        if form.is_valid():
            if request.FILES:
                profile = request.user.profile
                profile.image = request.FILES["image"]
                profile.save()
            else:
                profile = request.user.profile
                profile.image = None
                profile.save()
            return redirect("profile")
        else:
            messages.error(request, "Failed to update profile image, try again")
    else:
        form = UpdateImageForm()
    return render(request, "update_profile_image.html", {"form": form})
    
