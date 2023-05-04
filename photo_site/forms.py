from django import forms
from .models import Photo, Comment, Lens, get_lens_choices


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
            "lens_name",
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
            "lens_name": "Lens Name",
            "lens": "Lens Used",
            "keywords": "Keywords",
            "year_taken": "Year Taken",
        }
        choices = {"lens_name": get_lens_choices()}


class CommentForm(forms.ModelForm):
    """a form for creating a comment"""

    class Meta:
        model = Comment
        fields = ("comment",)

        labels = {
            "comment": "Comment",
        }


class LensForm(forms.ModelForm):
    """a form for adding new lens info"""

    class Meta:
        model = Lens
        fields = ("name",)
        labels = {
            "name": "Make/Model",
        }
