from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Users app models


class Profile(models.Model):
    """a profile to extend Django's built in User model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, blank=True, null=True)
    age = models.SmallIntegerField(blank=True, null=True)
    location_city = models.CharField(max_length=200, blank=True, null=True)
    location_state = models.CharField(max_length=200, blank=True, null=True)
    location_country = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    # called when new user saved to auto create profile
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # Saves the user profile info when user is saved
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f"{self.user}, {self.location_country}"
