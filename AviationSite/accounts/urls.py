from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views
from django.contrib.auth.views import auth_login

urlpatterns = [
    # login redirects to the built in accounts login page
    url(r'^login$', RedirectView.as_view(url='accounts/')),
    # home redirects to members home page
    url(r'^home$', views.membershome),
    # signup redirects to gliding signup page after a signup
    url(r'^signup$', views.signup),
    # signup redirects to gliding signup page before a signup
    url(r'^signuppage$', views.signuppage),
    # a blank url redirects to the main home page
    url(r'^$', RedirectView.as_view(url='home/'))
]
