from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
# from django.contrib.gis.geoip2 import GeoIP2

from user.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        bio = "This is an example of a bio"
        location = "Mexico"
        Profile.objects.create(user=instance, bio=bio, location=location)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
