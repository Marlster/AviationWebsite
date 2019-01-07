from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import BugReport
from .forms import BugReportForm
from common.utils import getcurrentdate

def reportabug(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST)
        if form.is_valid():
            newBug = form.save(commit=False)
            newBug.reporter = request.user
            newBug.date_reported = getcurrentdate()
            newBug.save()
            # TODO change this to redirect to a "your bug has been reported thanks" page
            return redirect('/home')
    # otherwise just returns the form
    else:
        form = BugReportForm()
    args = {'form': form}
    return render(request, 'bugs/reportabug.html', args)
