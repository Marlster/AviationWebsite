from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import modelformset_factory, BaseModelFormSet
from .models import GlidingSignup,GlidingSession,Profile
from .forms import SignupForm, NewSessionForm, ChooseSessionForm, FillForm
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
    if not request.user.is_superuser:
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
    if not request.user.is_superuser:
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
    # FillFormSet = modelformset_factory(GlidingSignup, form = FillForm, extra=session.attendees.count())
    # class FormSetWithInstances(BaseModelFormSet):
    #     def __init__(self, *args, **kwargs):
    #         self.instances = kwargs.pop('instances')
    #         super(FormSetWithInstances, self).__init__(*args, **kwargs)
    #     def get_form_kwargs(self, index):
    #         form_kwargs = super(FormSetWithInstances, self).get_form_kwargs(index)
    #         if index < len(self.instances):
    #             form_kwargs['instance'] = self.instances[index]
    #         return form_kwargs
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

        # try:
        # instances = session.glidingsignup_set.all()
        # formset = FillFormSet(request.POST, request.FILES)
        # except ValidationError:
        #     formset = None 