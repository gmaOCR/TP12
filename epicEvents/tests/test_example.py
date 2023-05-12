import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Client, Contract, Event
from .serializers import (
    ClientListSerializer,
    ClientSerializer,
    ContractListSerializer,
    ContractSerializer,
    ContractCreateSerializer,
    ContractUpdateSerializer,
    EventListSerializer,
    EventSerializer,
    EventCreateUpdateSerializer
)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create(username='testuser')

@pytest.fixture
def client():
    return Client.objects.create(name='Test Client')

@pytest.fixture
def contract(client, user):
    return Contract.objects.create(client=client, sales_contact=user)

@pytest.fixture
def event(client):
    return Event.objects.create(client=client, eventStatus='1')

@pytest.fixture
def client_data():
    return {
        'name': 'Test Client',
        'sales_contact': 1
    }

@pytest.fixture
def contract_data(client):
    return {
        'client': client.pk,
        'sales_contact': 1,
        'amount': 1000,
        'status': True,
        'paymentDue': '2023-05-10'
    }

@pytest.fixture
def event_data(client):
    return {
        'client': client.pk,
        'eventStatus': '1'
    }

@pytest.mark.django_db
class TestClientViewSet:
    def test_list_clients(self, api_client, client):
        url = reverse('client-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = ClientListSerializer([client], many=True)
        assert response.data == serializer.data

    def test_retrieve_client(self, api_client, client):
        url = reverse('client-detail', kwargs={'pk': client.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = ClientSerializer(client)
        assert response.data == serializer.data

    def test_create_client(self, api_client, user, client_data):
        url = reverse('client-list')
        api_client.force_authenticate(user=user)
        response = api_client.post(url, client_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Client.objects.count() == 1
        client = Client.objects.first()
        serializer = ClientSerializer(client)
        assert response.data['data'] == serializer.data

    def test_update_client(self, api_client, user, client):
        url = reverse('client-detail', kwargs={'pk': client.pk})
        api_client.force_authenticate(user=user)
        data = {'name': 'Updated Client'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        client.refresh_from_db()
        assert client.name == 'Updated Client'
        serializer = ClientSerializer(client)
        assert response.data['data'] == serializer.data

    def test_delete_client(self, api_client, user, client):
        url = reverse('client-detail', kwargs={'pk': client.pk})
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Client.objects.count() == 0

@pytest.mark.django_db
class TestContractViewSet:
    def test_list_contracts(self, api_client, client, contract):
        url = reverse('contract-list', kwargs={'client_id': client.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = ContractListSerializer([contract], many=True)
        assert response.data == serializer.data

    def test_retrieve_contract(self, api_client, client, contract):
        url = reverse('contract-detail', kwargs={'client_id': client.pk, 'pk': contract.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = ContractSerializer(contract)
        assert response.data == serializer.data

    def test_create_contract(self, api_client, user, client, contract_data):
        url = reverse('contract-list', kwargs={'client_id': client.pk})
        api_client.force_authenticate(user=user)
        response = api_client.post(url, contract_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Contract.objects.count() == 1
        contract = Contract.objects.first()
        serializer = ContractSerializer(contract)
        assert response.data['data'] == serializer.data

    def test_update_contract(self, api_client, user, client, contract):
        url = reverse('contract-detail', kwargs={'client_id': client.pk, 'pk': contract.pk})
        api_client.force_authenticate(user=user)
        data = {'amount': 2000}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        contract.refresh_from_db()
        assert contract.amount == 2000
        serializer = ContractSerializer(contract)
        assert response.data['data'] == serializer.data

    def test_delete_contract(self, api_client, user, client, contract):
        url = reverse('contract-detail', kwargs={'client_id': client.pk, 'pk': contract.pk})
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Contract.objects.count() == 0

@pytest.mark.django_db
class TestEventViewSet:
    def test_list_events(self, api_client, event):
        url = reverse('event-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = EventListSerializer([event], many=True)
        assert response.data == serializer.data

    def test_retrieve_event(self, api_client, event):
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = EventSerializer(event)
        assert response.data == serializer.data

    def test_create_event(self, api_client, user, client, event_data):
        url = reverse('event-list')
        api_client.force_authenticate(user=user)
        response = api_client.post(url, event_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1
        event = Event.objects.first()
        serializer = EventSerializer(event)
        assert response.data['data'] == serializer.data

    def test_update_event(self, api_client, user, event):
        url = reverse('event-detail', kwargs={'pk': event.pk})
        api_client.force_authenticate(user=user)
        data = {'eventStatus': '2'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        event.refresh_from_db()
        assert event.eventStatus == '2'
        serializer = EventSerializer(event)
        assert response.data['data'] == serializer.data

    def test_delete_event(self, api_client, user, event):
        url = reverse('event-detail', kwargs={'pk': event.pk})
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Event.objects.count() == 0

