from django import forms
from .models import Photo, Comment, Lens


class PhotoForm(forms.ModelForm):
    """a form to upload a new photo"""

    class Meta:
        model = Photo
        fields = (
            "image",
            "title",
            "description",
            "location",
            "camera",
            "keywords",
            "year_taken",
            "lens_used",
            "photo_type",
        )
        labels = {
            "image": "Image",
            "title": "Title",
            "description": "Description",
            "location": "Location",
            "camera": "Camera Used",
            "keywords": "Keywords",
            "year_taken": "Year Taken",
            "lens_used": "Lens Used",
            "photo_type": "Type of Photography",
        }


class CommentForm(forms.ModelForm):
    """a form for creating a comment"""

    class Meta:
        model = Comment
        fields = ("comment",)

        labels = {
            "comment": "Comment",
        }


class LensForm(forms.ModelForm):
    """a form for adding lens info"""

    class Meta:
        model = Lens
        fields = (
            "name",
            "make",
            "size",
        )
        labels = {
            "name": "Name",
            "make": "Make",
            "size": "Size",
        }
