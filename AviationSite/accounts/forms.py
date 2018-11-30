from django import forms
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
        self.fields['session'].queryset = GlidingSession.objects.filter(date__gte=datetime.date(year,month,day)).order_by('date')