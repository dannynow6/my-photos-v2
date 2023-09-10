from django.contrib import admin
from .models import Photo, Comment, Lens
from .utils import process_photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title")

    def save_model(self, request, obj, form, change):
        try:
            # check if image has been uploaded
            if "image" in form.changed_data:
                uploaded_image = form.cleaned_data["image"]
                if hasattr(uploaded_image, "read"):
                    processed_image = process_photo(uploaded_image)
                    obj.image = processed_image
                else:
                    print("Invalid file received", uploaded_image)
            # Save the photo model
            super().save_model(request, obj, form, change)
        except Exception as e:
            print("Error in save_model:", e)


# Register your models here.
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment)
admin.site.register(Lens)
