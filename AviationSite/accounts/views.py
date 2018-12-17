from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import GlidingSignup,GlidingSession,Profile
from .forms import SignupForm


def home(request):
    # numbers = [1, 2, 3, 4, 5]
    # name = 'Marley Chinn'
    # args = {'myName': name, 'numbers': numbers}
    return render(request, 'accounts/home.html')

def membershome(request):
    return render(request, 'accounts/memberpage.html')


def signuppage(request):
    # res = urlopen('http://just-the-time.appspot.com/')
    # result = res.read().strip()
    # result_str = result.decode('utf-8')
    # year = int(result_str[:4])
    # month = int(result_str[5:7])
    # day = int(result_str[8:10])
    # futureSessions = GlidingSession.objects.filter(date__gte=datetime.date(year,month,day)).order_by('date')
    # processes form data if its a POST request
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            newSignup = form.save(commit=False)
            newSignup.member = request.user.profile
            newSignup.save()
            # TODO change this to redirect to a "successful signup" page
            return redirect('/account/home')
    else:
        form = SignupForm()
    args = {'form': form}
    return render(request, 'accounts/glidingsignup.html',args)

def userdetails(request):
    return render(request, 'accounts/userdetails.html')
