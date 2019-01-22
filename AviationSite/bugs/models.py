from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.forms import ModelForm

BUG_PRIORITIES = (("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High"), ("CRITICAL", "Critical"), ("TBD", "TBD"))

class BugReport(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()
    environment = models.TextField()
    URL = models.URLField()
    screenshot_URL = models.URLField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter")
    severity = models.TextField(max_length = 10, default="TBD", choices=BUG_PRIORITIES)
    date_reported = models.DateField()
    fixed = models.BooleanField(default=False)
    date_fixed = models.DateField(null=True, blank=True)
    fixed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="fixer")
    def __str__(self):
        return self.date_reported
    class Meta:
        verbose_name = "Bug Report"