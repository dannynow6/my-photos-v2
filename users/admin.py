from django.contrib import admin
from .models import Profile
from .utils import process_image


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "age")

    def save_model(self, request, obj, form, change):
        try:
            # check if a new image has been uploaded
            if "photo" in form.changed_data:
                profile_photo = form.cleaned_data["photo"]
                if hasattr(profile_photo, "read"):
                    processed_image = process_image(profile_photo)
                    obj.photo = processed_image
                else:
                    print("Invalid file received", profile_photo)

            # save the model
            super().save_model(request, obj, form, change)
        except Exception as e:
            print("Error in save_model:", e)


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
