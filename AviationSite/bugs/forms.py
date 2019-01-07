from django import forms
from django.db.models import F, Count
from .models import BugReport

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ('name','description','environment','URL','screenshot_URL')
    # def __init__(self, *args, **kwargs):
    #     super(BugReportForm, self).__init__(*args, **kwargs)
    #     self.fields['date_fixed'].required = False
    #     self.fields['fixed_by'].required = False