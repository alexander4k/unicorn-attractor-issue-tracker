from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateImageForm
from django.http import Http404

@login_required    
def profile(request):
    # A view to display user's profile
    if not hasattr(request.user, 'profile'):
        raise Http404 
    else:
        profile = request.user.profile 
    return render(request, 'profile.html', {'profile': profile})

@login_required
def update_profile_image(request):
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
    
