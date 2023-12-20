from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator  # , EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Photo, Comment, Lens
from .forms import PhotoForm, CommentForm, LensForm
from users.models import Profile
import random
from users.forms import NewUserForm

# Imports for Manipulating and Normalizing Images
from .utils import process_photo

# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile


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
                # Get the uploaded image from the form
                uploaded_img = new_photo.image
                new_photo.image = process_photo(uploaded_img)
                new_photo.save()
                # create a success msg to notify user
                messages.success(request, "Your photo was saved successfully!")
                # redirect user to photos page
                return redirect("photo_site:photos")

            else:
                messages.error(
                    request,
                    "There was an error in the form submission. Please check your inputs.",
                )
                return redirect("photo_site:photos")
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
    # Get search value
    search_value = request.GET.get("SearchValue", "")
    # Get ID search value
    search_id = request.GET.get("photoID", "")

    if selected_type:
        photos = Photo.objects.filter(photo_type__iexact=selected_type).order_by(
            "-date_added"
        )

    elif search_value:
        photos = Photo.objects.filter(keywords__icontains=search_value).order_by(
            "-date_added"
        )

    elif search_id:
        photos = Photo.objects.filter(id__icontains=search_id).order_by("-date_added")

    else:
        photos = Photo.objects.order_by("-date_added")

    paginator = Paginator(photos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # build the query parameters for pagination links
    query_params = request.GET.copy()
    if "page" in query_params:
        del query_params["page"]

    context = {
        "photos": page_obj,  # this ensures that photos only pulled from one variable
        "selected_type": selected_type,
        "search_value": search_value,
        "search_id": search_id,
        "photo_types": Photo.TYPE_CHOICES,
        "page_obj": page_obj,
        "query_params": query_params.urlencode(),
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
                # create a success msg to notify user
                messages.success(request, "Your photo was successfully edited!")
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


"""
def search_photos(request):
    search_value = request.GET.get("SearchValue", "")

    try:
        photos = Photo.objects.filter(keywords__icontains=search_value)
    except ObjectDoesNotExist:
        error_msg = "There are no photos containing those keywords"
        messages.error(request, error_msg)
        context = {"error_msg": error_msg}
        return render(request, "search.html", context)

    context = {"photos": photos}
    return render(request, "search.html", context)
"""
