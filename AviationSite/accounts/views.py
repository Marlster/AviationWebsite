from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import GlidingSignup,GlidingSession,Profile
from .forms import SignupForm


class SignupDelete(DeleteView):
    model = GlidingSignup
    success_url = reverse_lazy('signups')

def home(request):
    # numbers = [1, 2, 3, 4, 5]
    # name = 'Marley Chinn'
    # args = {'myName': name, 'numbers': numbers}
    return render(request, 'accounts/home.html')

def membershome(request):
    return render(request, 'accounts/memberpage.html')


def signuppage(request):
    # processes form data if its a POST request
    if not request.user.is_authenticated:
        return render(request, 'accounts/memberpage.html')
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
        signid = (session.glidingsignup_set.get(member=request.user.profile)).pk 
        sessions.append([drivers,others,date,signid])
    args = {'form': form, 'sessions': sessions}
    return render(request, 'accounts/glidingsignup.html',args)

def userdetails(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/memberpage.html')
    return render(request, 'accounts/userdetails.html')

def settings(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/memberpage.html')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/account/settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/settings.html', {
        'form': form
    })