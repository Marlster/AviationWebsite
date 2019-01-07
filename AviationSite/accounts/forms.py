from django import forms
from django.db.models import F, Count
from .models import GlidingSignup, GlidingSession
from common.utils import getcurrentdate

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

# class CancelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
        