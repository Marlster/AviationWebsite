from django import forms
from django.db.models import F, Count
from .models import GlidingSignup, GlidingSession, Profile
from common.utils import getcurrentdate
import datetime

# make sure to pass the user as an argument so that it can be used to filter the results
class SignupForm(forms.ModelForm):
    class Meta:
        model = GlidingSignup
        fields = ('session',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(SignupForm, self).__init__(*args, **kwargs)
        # checks each session is in the future
        qs = GlidingSession.objects.filter(date__gte=getcurrentdate())
        # checks each session isn't cancelled
        qs = qs.filter(is_cancelled=False)
        # checks each session has a free space
        qs = qs.annotate(num_attendees=Count('attendees')).filter(num_attendees__lt=F('max_attendees'))
        # hecks that the user hasn't signed up to it already
        qs = qs.exclude(attendees__user=self.user)
        # orders the sessions by date
        qs = qs.order_by('date') 
        # returns the queryset of sessions to be used as the fields of the form
        self.fields['session'].queryset = qs

class NewSessionForm(forms.Form):
    date = forms.DateField(label = 'Session Date', widget=forms.widgets.SelectDateWidget())
    driver = forms.ModelChoiceField(queryset = Profile.objects.filter(can_drive=True))
    max_attendees = forms.IntegerField(max_value = 5)

    def clean_date(self):
        date = self.cleaned_data['date']
        # makes sure that the date is in the future
        if date <= datetime.date.today():
            raise forms.ValidationError("The date entered is in the past")
        # makes sure that there isn't already a session on that date
        if GlidingSession.objects.filter(date=date):
            raise forms.ValidationError("There is already a session on that day")
        return date

# input_formats = ['%d/%m/%y']