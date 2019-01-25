# Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
# Contrib stuff
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm
# Django Utils
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# Other Django Stuff
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import modelformset_factory, BaseModelFormSet
# Custom Stuff
from .models import GlidingSignup,GlidingSession,Profile
from .forms import SignupForm, NewSessionForm, ChooseSessionForm, FillForm, NewUserForm
from .tokens import account_activation_token
from common.utils import getcurrentdate

class SignupDelete(DeleteView):
    model = GlidingSignup
    success_url = reverse_lazy('signups')

def membershome(request):
    return render(request, 'accounts/memberpage.html')

def newuser(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = NewUserForm()
    return render(request, 'accounts/newuser.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'accounts/activate_message.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def signuppage(request):
    # processes form data if its a POST request
    # This bit processes the signup form for future sessions
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
    # this bit processes the data to be displayed in the current signups section
    currentSessions = GlidingSession.objects.filter(date__gte=getcurrentdate()).filter(attendees__user=request.user).filter(is_cancelled=False)
    cSessions = []
    for session in currentSessions:
        # NOTE could change to just a "2 spaces left" thing rather than names, will think about
        drivers = (session.glidingsignup_set.filter(is_driver=True))
        others = (session.glidingsignup_set.exclude(is_driver=True))
        date = (session.date)
        signid = (session.glidingsignup_set.get(member=request.user.profile)).pk 
        cSessions.append([drivers,others,date,signid])
    # this processes the data for the past signups section
    pastSessions = GlidingSession.objects.exclude(date__gte=getcurrentdate()).filter(attendees__user=request.user).filter(is_cancelled=False)
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
    if not request.user.is_staff:
        return render(request, 'accounts/memberpage.html')
    if request.method == 'POST':
        form = NewSessionForm(request.POST)
        ses = 0/0
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
    return render(request, 'accounts/newglidingsession.html', args)

def choosesession(request):
    if not request.user.is_staff:
        return render(request, 'accounts/memberpage.html')
    if request.method == 'POST':
        form = ChooseSessionForm(request.POST)
        if form.is_valid():
            session = form.cleaned_data['session']
            request.method = 'GET'
            return fillsession(request, session.pk)
    else:
        form = ChooseSessionForm()
    args = {'form': form}
    return render(request, 'accounts/choosesession.html', args)

def fillsession(request, pk=1):
    session=get_object_or_404(GlidingSession, id=pk) # gets the selected session
    if request.method == 'POST':
        form = FillForm(request.POST, attendees = session.attendees.all())
        if form.is_valid():
            for signup in session.glidingsignup_set.all():
                signup.total_launches = form.cleaned_data['total_launches %d' % signup.member.pk]
                signup.total_aerotows = form.cleaned_data['total_aerotows %d' % signup.member.pk]
                signup.total_minutes = form.cleaned_data['total_minutes %d' % signup.member.pk]
                signup.save()
            session.filled = True
            session.save()
            return redirect('/account/choosesession')
    else:
        form = FillForm(attendees = session.attendees.all())
    attendees = []
    for attendee in session.attendees.all():
        fields = form.get_member_fields(attendee)
        attendees.append([attendee,fields])
    args = {'session': session, 'attendees': attendees}
    return render(request, 'accounts/fillsession.html', args)
