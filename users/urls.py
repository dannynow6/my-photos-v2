""" Defines URL patterns for Users App """
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    # include default auth urls
    path("", include("django.contrib.auth.urls")),
    # Registration
    path("register/", views.register, name="register"),
    # User profile
    path("profile/<int:user_id>/", views.profile, name="profile"),
    # View user profile details
    path("view_profile/<int:user_id>/", views.view_profile, name="view_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
