from django.shortcuts import render
from django.contrib.auth.models import User
from .models import HomepageVersion, TextSection

# Create your views here.

def home(request):
    currentVersion = HomepageVersion.objects.get(current_version = True)
    args = {"textsections": currentVersion, "user": request.user}
    return render(request, 'home/home.html', args)

def success(request):
    args = {"user": request.user}
    return render(request, 'home/success.html', args)
