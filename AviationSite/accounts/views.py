from django.shortcuts import render
from django.contrib.auth.models import User
from .models import GlidingSignup,GlidingSession,Profile
from urllib.request import urlopen
import datetime

# Create your views here.
def home(request):
    # numbers = [1, 2, 3, 4, 5]
    # name = 'Marley Chinn'
    # args = {'myName': name, 'numbers': numbers}
    return render(request, 'accounts/home.html')

def membershome(request):
    return render(request, 'accounts/memberpage.html')

def signup(request):
    currentUserProfile = request.user.get_profile()
  #  newSignup = GlidingSignup.objects.create(member=currentUserProfile,session=*TODO*,is_driver=0,total_launches=0,total_aerotows=0,total_minutes=0)
   # {{ user.username }}
    return render(request, 'accounts/glidingsignup.html')

def signuppage(request):
    # gets current date/time from the web
    # NOTE: may break if the website it gets the time from goes down (or changes format)
    res = urlopen('http://just-the-time.appspot.com/')
    result = res.read().strip()
    result_str = result.decode('utf-8')
    year = int(result_str[:4])
    month = int(result_str[5:7])
    day = int(result_str[8:10])
    futureSessions = GlidingSession.objects.filter(date__gte=datetime.date(year,month,day)).order_by('date')
    args = {'futureSessions': futureSessions}
    return render(request, 'accounts/glidingsignup.html',args)
