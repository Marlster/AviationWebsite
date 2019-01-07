from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import BugReport
from .forms import BugReportForm
from urllib.request import urlopen
import datetime

def reportabug(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST)
        if form.is_valid():
            newBug = form.save(commit=False)
            newBug.reporter = request.user
            # date stuff
            res = urlopen('http://just-the-time.appspot.com/')
            result = res.read().strip()
            result_str = result.decode('utf-8')
            current_date = datetime.date(int(result_str[:4]),int(result_str[5:7]),int(result_str[8:10]))
            newBug.date_reported = current_date
            newBug.save()
            # TODO change this to redirect to a "your bug has been reported thanks" page
            return redirect('/home')
    # otherwise just returns the form
    else:
        form = BugReportForm()
    args = {'form': form}
    return render(request, 'bugs/reportabug.html', args)
