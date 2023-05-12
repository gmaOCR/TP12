from django.contrib import admin
from .models import Client, Contract, Event
from .views import ClientViewSet, ContractViewSet, EventViewSet


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'first_name', 'last_name', 'email', 'sales_contact')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('sales_contact',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'client', 'sales_contact', 'dateCreated', 'status', 'amount', 'paymentDue')
    search_fields = ('client__first_name', 'client__last_name', 'sales_contact__username')
    list_filter = ('status', 'sales_contact')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'eventStatus', 'support_contact', 'eventDate', 'attendes')
    search_fields = ('eventStatus__client__first_name', 'eventStatus__client__last_name', 'support_contact__username')
    list_filter = ('eventStatus', 'support_contact')


