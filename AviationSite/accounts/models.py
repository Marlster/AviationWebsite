from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length = 500, blank = True)

    def __unicode__(self):
        return self.name

class GlidingSession(models.Model):
    attendees = models.ManyToManyField(Profile, through='GlidingSignup')
    date = models.DateField()
    is_cancelled = models.BooleanField()
    class Meta:
        verbose_name = "Gliding Session"
    def __unicode__(self):
        return self.name

class GlidingSignup(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session = models.ForeignKey(GlidingSession, on_delete=models.CASCADE)
    is_driver = models.BooleanField()
    total_launches = models.IntegerField()
    total_aerotows = models.IntegerField()
    total_minutes = models.IntegerField()

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


