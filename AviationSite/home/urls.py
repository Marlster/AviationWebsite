from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # a blank url displays the home page
    url(r'^success$', views.success),
    url(r'^trials$', views.trials),
    url(r'^$', views.home)
]