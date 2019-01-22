from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import GlidingSignup,GlidingSession,Profile
from .forms import SignupForm, NewSessionForm
from common.utils import getcurrentdate

class SignupDelete(DeleteView):
    model = GlidingSignup
    success_url = reverse_lazy('signups')

# class SessionCreate(CreateView):
#     model = GlidingSession
#     fields = ['date']

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
    currentSessions = GlidingSession.objects.filter(date__gte=getcurrentdate()).filter(attendees__user=request.user).filter(is_cancelled=False)
    pastSessions = GlidingSession.objects.exclude(date__gte=getcurrentdate()).filter(attendees__user=request.user).filter(is_cancelled=False)
    cSessions = []
    for session in currentSessions:
        # NOTE could change to just a "2 spaces left" thing rather than names, will think about
        drivers = (session.glidingsignup_set.filter(is_driver=True))
        others = (session.glidingsignup_set.exclude(is_driver=True))
        date = (session.date)
        signid = (session.glidingsignup_set.get(member=request.user.profile)).pk 
        cSessions.append([drivers,others,date,signid])
    args = {'form': form, 'sessions': cSessions, 'past_sessions': pastSessions}
    return render(request, 'accounts/glidingsignup.html', args)

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

def newsession(request):
    if not request.user.is_superuser:
        return render(request, 'accounts/memberpage.html')
    if request.method == 'POST':
        form = NewSessionForm(request.POST)
        if form.is_valid():
            newSession = GlidingSession(date = form.cleaned_data['date'])
            newSession.max_attendees = int(form.cleaned_data['max_attendees'])
            newSession.save()
            newSignup = GlidingSignup(session = newSession, member = form.cleaned_data['driver'])
            newSignup.is_driver = True
            newSignup.save()
            return redirect('/account/signuppage')
    else:
        form = NewSessionForm()
    args = {'form': form}
    return render(request, 'accounts/glidingsession_form.html', args)