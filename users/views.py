from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import NewUserForm, ProfileForm

# Imports for Manipulating and Normalizing Images
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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


def process_image(profile_img):
    """process profile image"""
    # Get the uploaded image from the form
    profile_image = profile_img
    # Open the uploaded image using Pillow
    image = Image.open(profile_image)
    # Resize the image to max height/width of 125px
    max_size = (125, 125)
    image.thumbnail(max_size)
    # Create a BytesIO buffer to temporarily store image
    image_buffer = BytesIO()
    image.save(image_buffer, format="JPEG")
    # Create an InMemoryUploadedFile from the buffer
    image_file = InMemoryUploadedFile(
        image_buffer,
        None,
        f"{profile_img.name}.jpg",
        "image/jpeg",
        image_buffer.tell(),
        None,
    )
    # Return processed image
    return image_file


def view_profile(request, user_id):
    """User can view detailed profile info"""
    profile = Profile.objects.get(user=user_id)
    # Handle form for edit profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # new_profile = form.save(commit=False)
            # profile_photo = new_profile.photo
            # new_profile.photo = process_image(profile_photo)
            # Check if 'photo' field has changed data
            if "photo" in form.changed_data:
                # Compare file paths or urls of uploaded picture and existing picture
                uploaded_pic = (
                    form.cleaned_data["photo"].name
                    if form.cleaned_data["photo"]
                    else None
                )
                existing_pic = profile.photo.name if profile.photo else None

                if uploaded_pic == existing_pic:
                    # if the urls match, don't save the file
                    if existing_pic:
                        profile.photo.delete(save=False)
                    form.cleaned_data["photo"] = None
                    form.save()
                    return redirect("users:view_profile", user_id=user_id)
                else:
                    # Get uploaded image
                    profile_photo = form.photo
                    # process uploaded image and save processed image
                    form.photo = process_image(profile_photo)
                    form.save()
                    return redirect("users:view_profile", user_id=user_id)
    else:
        # display a blank form
        form = ProfileForm(instance=profile)

    context = {"profile": profile, "form": form}
    return render(request, "registration/view_profile.html", context)
