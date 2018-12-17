from django import forms
from django.db.models import F, Count
from .models import GlidingSignup, GlidingSession
from urllib.request import urlopen
import datetime

class SignupForm(forms.ModelForm):
    class Meta:
        model = GlidingSignup
        fields = ('session',)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # gets current date/time from the web
        # NOTE: may break if the website it gets the time from goes down (or changes format)
        res = urlopen('http://just-the-time.appspot.com/')
        result = res.read().strip()
        result_str = result.decode('utf-8')
        year = int(result_str[:4])
        month = int(result_str[5:7])
        day = int(result_str[8:10])
        # checks each session is in the future
        qs = GlidingSession.objects.filter(date__gte=datetime.date(year,month,day))
        # checks each session isn't cancelled
        qs = qs.filter(is_cancelled=False)
        # checks each session has a free space
        qs = qs.annotate(num_attendees=Count('attendees')).filter(num_attendees__lt=F('max_attendees'))
        # TODO checks that the user hasn't signed up to it already
        # orders the sessions by date
        qs = qs.order_by('date') 
        # returns the queryset of sessions to be used as the fields of the form
        self.fields['session'].queryset = qs