from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    
    # each profile is linked to the Django User via OneToOne relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # WG's player id
    player_id = models.IntegerField(null=True, blank=True)

    # clan info
    clan_tag = models.CharField(null=True, blank=True, max_length=5)
    clan_id = models.IntegerField(null=True, blank=True)

    # ships?
    # player CB preferences?


# create a profile whenever a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) 

# save changes to profile whenever User is changed
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()