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
    # processes form data if its a POST request
    if request.method == 'POST':
        form = SignupForm(request.POST,user=request.user)
        if form.is_valid():
            newSignup = form.save(commit=False)
            newSignup.member = request.user.profile
            newSignup.save()
            # TODO change this to redirect to a "successful signup" page
            return redirect('/account/home')
    # otherwise just returns the form
    else:
        form = SignupForm(user=request.user)
    # also gets currently signed up to sessions that aren't cancelled
    currentSessions = GlidingSession.objects.filter(attendees__user=request.user).filter(is_cancelled=False)
    sessions = []
    for session in currentSessions:
        drivers = (session.glidingsignup_set.filter(is_driver=True))
        others = (session.glidingsignup_set.exclude(is_driver=True))
        date = (session.date)
        sessions.append([drivers,others,date])
    args = {'form': form, 'sessions': sessions}
    return render(request, 'accounts/glidingsignup.html',args)

def userdetails(request):
    return render(request, 'accounts/userdetails.html')
