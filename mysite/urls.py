"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from hijack import urls

from django.urls import path
from mysite.core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', core_views.home, name='home'),
    url(r'^$', auth_views.login, name='home'),
    url(r'^terms/$', auth_views.login, name='terms'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^account_activation_resent/$', core_views.account_activation_resent, name='account_activation_resent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^trips/', include('trips.urls', namespace='trips')),
    url(r'^hijack/', include('hijack.urls', namespace='hijack')),
    # url(r'^avatar/', include('avatar.urls')),
]
