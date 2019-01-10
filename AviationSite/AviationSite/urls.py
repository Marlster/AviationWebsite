"""AviationSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # displays a static home page
    path('home/', include('home.urls')),
    # redirects to the built in accounts module (which lets users login/logout)
    path('accounts/', include('django.contrib.auth.urls')),
    # redirects to the urls in the account app
    path('account/', include('accounts.urls'), name = 'accounts'),
    # redirects to the urls in the bug reporting app
    path('reportabug/', include('bugs.urls'), name = 'bugs'),
    # used for the admin portal
    path('admin/', admin.site.urls),
    # blank url redirects as home
    path('', RedirectView.as_view(url='/home/'), name='home')
]
# TemplateView.as_view(template_name='accounts/memberpage.html'