from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import NewUserForm, ProfileForm

# Imports for Manipulating and Normalizing Images
from .utils import process_image

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


def view_profile(request, user_id):
    """User can view detailed profile info"""
    profile = Profile.objects.get(user=user_id)
    # Handle form for edit profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            profile_photo = new_profile.photo

            # Check if uploaded image is same as existing one
            if profile_photo:
                if profile_photo.read() != profile.photo.read():
                    new_profile.photo = process_image(profile_photo)
                else:
                    # If images are the same, use the existing one
                    new_profile.photo = profile.photo

            form.save()
            return redirect("users:view_profile", user_id=user_id)
    else:
        # display a blank form
        form = ProfileForm(instance=profile)

    context = {"profile": profile, "form": form}
    return render(request, "registration/view_profile.html", context)
