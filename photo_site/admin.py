from django.contrib import admin
from .models import Photo, Comment, Lens
from .utils import process_photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "photo_type")
    list_filter = ("owner", "photo_type", "year_taken")
    search_fields = ("id", "title")

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


class LensAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "size")
    list_filter = ("make",)
    search_fields = ("size",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("owner", "date_added", "photo")
    list_filter = ("owner",)
    search_fields = ("comment",)


# Register your models here.
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Lens, LensAdmin)
