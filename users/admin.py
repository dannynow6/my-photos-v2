from django.contrib import admin
from .models import Profile
from .utils import process_image


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "age")

    def save_model(self, request, obj, form, change):
        # check if a new image has been uploaded
        if "photo" in form.changed_data:
            profile_photo = form.cleaned_data["photo"]
            processed_image = process_image(profile_photo)
            obj.photo = processed_image

        # save the model
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
