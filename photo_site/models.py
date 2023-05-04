from django.db import models
from django.contrib.auth.models import User


class Lens(models.Model):
    """a test to create a dynamic choices list for photo model"""

    name = models.CharField(max_length=125)

    def __str__(self):
        return f"{self.id}, {self.name}"


def get_lens_choices():
    lenses = Lens.objects.all()
    return [(l.id, l.name) for l in lenses] 

class Photo(models.Model):
    """a model representation of a photo"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="photos/")
    location = models.CharField(max_length=200, blank=True, null=True)
    camera = models.CharField(max_length=125, blank=True, null=True)
    lens_name = models.CharField(max_length=100, choices=(), null=True, blank=True)
    lens = models.CharField(max_length=200, blank=True, null=True)
    keywords = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    year_taken = models.CharField(max_length=10, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Photo, self).__init__(*args, **kwargs) 
        self._meta.get_field('lens_name').choices = get_lens_choices() 

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


# Create dynamic choice fields for photo model by creating additional models to store
# choice info. Users will be able to enter new choices not found in list.
