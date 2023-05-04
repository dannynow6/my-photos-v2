from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    """a custom new user form that extends Django's built in form"""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "bio",
            "age",
            "location_city",
            "location_state",
            "location_country",
            "photo",
        )
        labels = {
            "bio": "Short Bio",
            "age": "Age",
            "location_city": "City",
            "location_state": "State",
            "location_country": "Country",
            "photo": "Photo",
        }
