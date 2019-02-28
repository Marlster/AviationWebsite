from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views
from django.contrib.auth.views import auth_login

urlpatterns = [
    # login redirects to the built in accounts login page
    url(r'^login$', RedirectView.as_view(url='accounts/')),
    # home redirects to members home page
    url(r'^home$', views.membershome, name = "home"),
    # signup redirects to gliding signup page after a signup
    url(r'^signuppage$', views.signuppage, name="signups"),
    # newuser redirects the user to the account creation page
    url(r'^newuser$', views.newuser),
    # sends the user to page telling them to confirm their email
    url(r'^account_activation_sent$', views.account_activation_sent, name='account_activation_sent'),
    # a url which confirms a user's email address and activates their account
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', views.activate, name='activate'),
    # details redirects to the user profile page
    url(r'^details$', views.userdetails),
    # settings redirects to the user settings page
    url(r'^settings$', views.settings),
    # newsession redirects to the admin form for creating a new gliding session
    url(r'^newsession$', views.newsession),
    # choosesession redirects to the admin form for choosing a past session to fill
    # which then redirects to the admin form for filling in a past session's gliding times
    url(r'^choosesession$', views.choosesession),
    # used for the fill session form
    path('fillsession/<int:pk>', views.fillsession, name="fill_session"),
    # updatehome redirects to the admin form for updating the text on the home page
    url(r'^updatehome$', views.newsession),
    # deletes a sign up
    path('<int:pk>/delete', views.SignupDelete.as_view(), name="signup_delete"),
    # a blank url redirects to the main home page
    url(r'^$', RedirectView.as_view(url='home/'))
]
