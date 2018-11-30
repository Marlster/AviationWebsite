from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GlidingSession,GlidingSignup,Profile

admin.site.register(GlidingSession)
admin.site.register(GlidingSignup)
admin.site.register(Profile)