from django.shortcuts import render
from .models import HomepageVersion, TextSection

# Create your views here.

def home(request):
    currentVersion = HomepageVersion.objects.get(current_version = True)
    args = {"textsections": currentVersion}
    return render(request, 'home/home.html', args)
