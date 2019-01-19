from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TextSection(models.Model):
	text = models.TextField()
	author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	date_created = models.DateField()

class HomepageVersion(models.Model):
	version_name = models.CharField(max_length = 20)
	current_version = models.BooleanField()
	our_story = models.ForeignKey(TextSection, on_delete=models.CASCADE, related_name = "story")
	events = models.ForeignKey(TextSection, on_delete=models.CASCADE, related_name = "events")
	trial_sessions = models.ForeignKey(TextSection, on_delete=models.CASCADE, related_name = "trials")
	join_us = models.ForeignKey(TextSection, on_delete=models.CASCADE, related_name = "join")