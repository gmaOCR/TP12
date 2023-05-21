"""
URL configuration for epicEvents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path

from rest_framework import routers

from sales.views import ClientViewSet, ContractViewSet, EventViewSet, ContractFilterViewset, EventFilterViewset, \
    ClientFilterViewset, not_found_view

router = routers.SimpleRouter()

router.register(r'client', ClientViewSet, basename='client')
router.register(r'client/(?P<client_id>\d+)/contract', ContractViewSet, basename='contract')
router.register(r'client/(?P<client_id>\d+)/contract/(?P<contract_id>\d+)/event', EventViewSet, basename='event')
router.register(r'contracts', ContractFilterViewset, basename='contracts')
router.register(r'events', EventFilterViewset, basename='events')
router.register(r'clients', ClientFilterViewset, basename='clients')

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    re_path(r'^(?!sales/|auth/|authentication/|logout|login).*/$', not_found_view),
    path('', admin.site.urls, name="login"),
]
urlpatterns += staticfiles_urlpatterns()