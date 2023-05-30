from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Photo, Comment, Lens
from .forms import PhotoForm, CommentForm, LensForm
from users.models import Profile
import random
from users.forms import NewUserForm


# Views for photo_site App

# View for Page Not Found Error
def ps_page_not_found(request, exception):
    context = {
        "error_message": "Page not found",
        "error_code": 404,
    }
    return render(request, "404.html", context, status=404)


def index(request):
    """home page for photo_site"""
    photos = Photo.objects.all()
    x = random.randint(1, len(photos))
    photo_id = x
    try:
        photo = Photo.objects.get(id=photo_id)  # get Photo with id = x
    except Photo.DoesNotExist:  # redo if photo with id doesn't exist
        z = random.randint(1, len(photos))
        while z == x:
            z = random.randint(1, len(photos))
        photo_id = z
        photo = Photo.objects.get(id=photo_id)
    y = random.randint(1, len(photos))
    # If y is the same as x, generate a new number
    while y == x:
        y = random.randint(1, len(photos))
    photo2_id = y
    try:
        photo2 = Photo.objects.get(id=photo2_id)  # get photo with id = y
    except Photo.DoesNotExist:
        w = random.randint(1, len(photos))
        while w == y or w == x:
            w = random.randint(1, len(photos))
        photo2_id = w
        photo2 = Photo.objects.get(id=photo2_id)
    # Handle New User registration form in Modal
    if request.method == "POST":
        # Process form data
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            # log user in and redirect to home page
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("photo_site:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    else:
        form = NewUserForm()
    context = {"photo": photo, "photo2": photo2, "form": form}
    return render(request, "photo_site/index.html", context)


# Require users to have an account before uploading a photo
@login_required
def add_photo(request):
    """a page for adding a new photo and a modal to add a new lens option"""
    photo_form = PhotoForm()
    lens_form = LensForm()

    if request.method == "POST":
        # Handle the add photo form
        if "add_photo_submit" in request.POST:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                new_photo = photo_form.save(commit=False)
                new_photo.owner = request.user
                new_photo.save()
                return redirect("photo_site:index")
        # Handle the add lens form
        elif "add_lens_submit" in request.POST:
            lens_form = LensForm(request.POST)
            if lens_form.is_valid():
                try:
                    lens_form.save()
                    return redirect("photo_site:add_photo")
                except IntegrityError:
                    lens_form.add_error("name", "This name already exists.")

    context = {"photo_form": photo_form, "lens_form": lens_form}
    return render(request, "photo_site/add_photo.html", context)


def photos(request):
    """Photos gallery page - allow users to filter results based on photo_type"""
    # Get the selected photo_type from query parameters
    selected_type = request.GET.get("photo_type")
    # Retrieve all photos if no type selected, otherwise filter photos by selected type
    if selected_type:
        photos = Photo.objects.filter(photo_type__iexact=selected_type).order_by(
            "-date_added"
        )
    else:
        photos = Photo.objects.order_by("-date_added")

    context = {
        "photos": photos,
        "selected_type": selected_type,
        "photo_types": Photo.TYPE_CHOICES,
    }
    return render(request, "photo_site/photos.html", context)


@login_required
def photo(request, photo_id):
    """Show the details of a specific photo"""
    current_user = request.user
    # Try to find photo matching id number
    try:
        photo = Photo.objects.get(id=photo_id)
    # If no photo with photo_id raise 404 error
    except Photo.DoesNotExist:
        raise Http404(f"Photo {photo_id} does not exist")

    comments = photo.comment_set.order_by("-date_added")
    paginator = Paginator(comments, 5)  # Show 5 comments per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Handle CommentForm and PhotoForm modals
    comment_form = CommentForm()
    photo_form = PhotoForm(instance=photo)
    if request.method == "POST":
        # Handle CommentForm submission
        if "add_comment" in request.POST:
            # POST data submitted and process data
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.photo = photo
                new_comment.owner = request.user
                new_comment.save()
                return redirect("photo_site:photo", photo_id=photo_id)
        # Handle PhotoForm submission
        elif "edit_photo" in request.POST:
            # POST data submitted and process data
            photo_form = PhotoForm(request.POST, request.FILES, instance=photo)
            if photo_form.is_valid():
                photo_form.save()
                return redirect("photo_site:photo", photo_id=photo_id)

    context = {
        "photo": photo,
        "current_user": current_user,
        "comments": comments,
        "page_obj": page_obj,
        "comment_form": comment_form,
        "photo_form": photo_form,
    }
    return render(request, "photo_site/photo.html", context)


@login_required
def my_photos(request):
    """display all photos uploaded by user"""
    # Allow user to filter results by photo_type
    selected_type = request.GET.get("photo_type")
    current_profile = Profile.objects.get(user=request.user)
    # Retrieve all photos of current user or photos of certain type
    if selected_type:
        my_photos = (
            Photo.objects.filter(photo_type__iexact=selected_type)
            .filter(owner=request.user)
            .order_by("-date_added")
        )
    else:
        my_photos = Photo.objects.filter(owner=request.user).order_by("-date_added")

    context = {
        "my_photos": my_photos,
        "current_profile": current_profile,
        "selected_type": selected_type,
        "photo_types": Photo.TYPE_CHOICES,
    }
    return render(request, "photo_site/my_photos.html", context)


@login_required
def edit_photo(request, photo_id):
    """User can edit their own photo"""
    photo = Photo.objects.get(id=photo_id)

    if request.method != "POST":
        form = PhotoForm(instance=photo)
    else:
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect("photo_site:my_photos")
    context = {"form": form, "photo": photo}
    return render(request, "photo_site/edit_photo.html", context)


# Since pulling photo from database for featured on About and Home pages
# Should handle potential error if no PK matches random number
# The problem could arise if a photo deleted or something
# Use a try/except block - with exception just add to the value and try again
def about(request):
    """An about page featuring basic site information for photo-site"""
    photos = Photo.objects.all()
    x = random.randint(1, len(photos))
    # Try to get photo with id = x
    try:
        photo = Photo.objects.get(id=x)
    # if photo with id = x no longer exists, generate new number
    except Photo.DoesNotExist:
        y = random.randint(1, len(photos))
        while y == x:
            y = random.randint(1, len(photos))
        photo = Photo.objects.get(id=y)
    context = {"photo": photo}
    return render(request, "photo_site/about.html", context)
