from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "photo_site"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    # Add photo page
    path("add_photo/", views.add_photo, name="add_photo"),
    # View photos uploaded by users
    path("photos/", views.photos, name="photos"),
    # View details of a specific photo
    path("photo/<int:photo_id>/", views.photo, name="photo"),
    # display all of a user's photos
    path("my_photos/", views.my_photos, name="my_photos"),
    # page for user to edit their photo
    path("edit_photo/<int:photo_id>/", views.edit_photo, name="edit_photo"),
    # about page for photo site 
    path("about/", views.about, name="about"), 
    # create a new comment on a photograph 
    path("comment/<int:photo_id>/", views.comment, name="comment"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
