from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # displays the bug report form
    url(r'^$', views.reportabug)
]