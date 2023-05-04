from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import NewUserForm, ProfileForm

# Views for Users App


def register(request):
    """Register a new User"""
    if request.method != "POST":
        # Display a blank form
        form = NewUserForm()
    else:
        # Process form data
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            # log user in and redirect to home page
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("photo_site:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    # display a blank or invalid form
    context = {"form": form}
    return render(request, "registration/register.html", context)


def profile(request, user_id):
    """user edit profile page"""
    profile = Profile.objects.get(user=user_id)
    if request.method != "POST":
        # display a blank form
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.save()
            return redirect("photo_site:index")
    context = {"profile": profile, "form": form}
    return render(request, "registration/profile.html", context)


def view_profile(request, user_id):
    """User can view detailed profile info"""
    profile = Profile.objects.get(user=user_id)
    context = {"profile": profile}
    return render(request, "registration/view_profile.html", context)
