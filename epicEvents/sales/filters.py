import django_filters
from .models import Contract, Event, Client


class ClientFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['last_name', 'email']


class ContractFilter(django_filters.FilterSet):
    client_last_name = django_filters.CharFilter(field_name='client__last_name', lookup_expr='icontains')
    client_email = django_filters.CharFilter(field_name='client__email', lookup_expr='icontains')
    dateCreated = django_filters.DateFilter(field_name='dateCreated', lookup_expr='icontains')
    amount = django_filters.NumberFilter()

    class Meta:
        model = Contract
        fields = ['client_last_name', 'client_email', 'dateCreated', 'amount']


class EventFilter(django_filters.FilterSet):
    client_last_name = django_filters.CharFilter(field_name='client__last_name', lookup_expr='icontains')
    client_email = django_filters.CharFilter(field_name='client__email', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['client_last_name', 'client_email', 'eventDate']
