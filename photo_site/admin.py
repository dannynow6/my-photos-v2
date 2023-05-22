from django.contrib import admin
from .models import Photo, Comment, Lens

# Register your models here.
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Lens) 
