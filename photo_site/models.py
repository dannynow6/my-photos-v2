from django.db import models
from django.contrib.auth.models import User


class Lens(models.Model):
    """Lens used to take photo"""

    name = models.CharField(max_length=150)
    make = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "lenses"

    def __str__(self):
        return f"{self.make}, {self.name}"


class Photo(models.Model):
    """a model representation of a photo"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="photos/")
    location = models.CharField(max_length=200, blank=True, null=True)
    camera = models.CharField(max_length=125, blank=True, null=True)
    lens = models.CharField(max_length=200, blank=True, null=True)
    keywords = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    year_taken = models.CharField(max_length=10, blank=True, null=True)
    lens_used = models.ForeignKey(Lens, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.owner}, {self.title}"


class Comment(models.Model):
    """User comment on photos"""

    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment[:50]}..."
