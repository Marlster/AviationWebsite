from django import forms
from django.db.models import F, Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GlidingSignup, GlidingSession, Profile
from common.utils import getcurrentdate

class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please input a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

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
        if date <= getcurrentdate():
            raise forms.ValidationError("The date entered is in the past")
        # makes sure that there isn't already a session on that date
        if GlidingSession.objects.filter(date=date):
            raise forms.ValidationError("There is already a session on that day")
        return date

class FillForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.attendees = kwargs.pop('attendees', None)
        super(FillForm, self).__init__(*args, **kwargs)
        for member in self.attendees:
            self.fields['total_launches %d' % member.pk] = forms.IntegerField(max_value = 10, label = 'Winch Launches:')
            self.fields['total_aerotows %d' % member.pk] = forms.IntegerField(max_value = 10, label = 'Aerotows:')
            self.fields['total_minutes %d' % member.pk] = forms.IntegerField(max_value = 500, label = 'Minutes In Flight:')
    def get_member_fields(self, member):
        for field_name in self.fields:
            if field_name.endswith(str(member.pk)):
                yield self[field_name]
    # def get_minute_fields(self):
    #     for field_name in self.fields:
    #         if field_name.startswith('total_minutes'):
    #             yield self[field_name]
    # class Meta:
    #     model = GlidingSignup
    #     fields = ('total_launches', 'total_aerotows', 'total_minutes',)
    # launches = forms.IntegerField(max_value = 10)
    # aerotows = forms.IntegerField(max_value = 10)
    # minutes = forms.IntegerField(max_value = 500)

class ChooseSessionForm(forms.Form):
    # gets the past unfilled sessions and checks session wasnt empty
    session = forms.ModelChoiceField(queryset = GlidingSession.objects.exclude(date__gt=getcurrentdate()).filter(is_cancelled=False).filter(filled=False).annotate(num_attendees=Count('attendees')).filter(num_attendees__gte=1))

# input_formats = ['%d/%m/%y']
# datetime.date.today()