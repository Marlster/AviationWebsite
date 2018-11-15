from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views
from django.contrib.auth.views import auth_login

urlpatterns = [
    url(r'^login$', RedirectView.as_view(url='accounts/')),
    url(r'^$', views.home),
]
