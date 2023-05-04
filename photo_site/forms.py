from django import forms
from .models import Photo, Comment


class PhotoForm(forms.ModelForm):
    """a form to upload a new photo"""

    class Meta:
        model = Photo
        fields = (
            "title",
            "description",
            "type",
            "image",
            "location",
            "camera",
            "lens",
            "keywords",
            "year_taken",
        )
        labels = {
            "title": "Title",
            "description": "Description",
            "type": "Type",
            "image": "Image",
            "location": "Location",
            "camera": "Camera Used",
            "lens": "Lens Used",
            "keywords": "Keywords",
            "year_taken": "Year Taken",
        }


class CommentForm(forms.ModelForm):
    """a form for creating a comment"""

    class Meta:
        model = Comment
        fields = ("comment",)

        labels = {
            "comment": "Comment",
        }
