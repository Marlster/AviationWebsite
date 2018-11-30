from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length = 500, blank = True)

    def __unicode__(self):
        return self.name

class GlidingSession(models.Model):
    attendees = models.ManyToManyField(Profile, through='GlidingSignup')
    date = models.DateField()
    max_attendees = models.IntegerField(default = 5)
    is_cancelled = models.BooleanField()
    class Meta:
        verbose_name = "Gliding Session"
    def __unicode__(self):
        return self.name

class GlidingSignup(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session = models.ForeignKey(GlidingSession, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default = False)
    total_launches = models.IntegerField(default = 0)
    total_aerotows = models.IntegerField(default = 0)
    total_minutes = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


