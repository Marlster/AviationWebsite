from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank = True)
    account_no = models.CharField(max_length = 10, blank = True)
    can_drive = models.BooleanField(default = False)
    paid_member = models.BooleanField(default = False)
    def __str__(self):
        return self.user.username

class GlidingSession(models.Model):
    attendees = models.ManyToManyField(Profile, through='GlidingSignup')
    date = models.DateField()
    max_attendees = models.IntegerField(default = 5)
    is_cancelled = models.BooleanField(default = False)
    filled = models.BooleanField(default = False)
    class Meta:
        verbose_name = "Gliding Session"
    def __str__(self):
        return str(self.date)

class GlidingSignup(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session = models.ForeignKey(GlidingSession, on_delete=models.CASCADE)
    # NOTE could add is_leader for the session leader (ie the committee member running it)
    # then it can display the leader on the signup page
    is_driver = models.BooleanField(default = False)
    total_launches = models.IntegerField(default = 0)
    total_aerotows = models.IntegerField(default = 0)
    total_minutes = models.IntegerField(default = 0)

    def __str__(self):
        return self.member.user.username + ' ' + str(self.session.date)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


