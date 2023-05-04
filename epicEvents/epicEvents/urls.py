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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from authentication.views import home, logout_view
from sales.views import staff, clients, contracts, events, create_client, edit_client, delete_client, create_contract




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('staff/', staff, name='staff'),
    path('clients/', clients, name='clients'),
    path('client/create/', create_client, name='create-client'),
    path('client/<int:client_id>/edit', edit_client, name='edit-client'),
    path('client/<int:client_id>/delete', delete_client, name='delete-client'),
    path('contracts/', contracts, name='contracts'),
    path('contract/create/', create_contract, name='create-contract'),
    path('events/', events, name='events'),
]

#if settings.DEBUG:
#    urlpatterns += static(
#        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)