import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from sales.models import Client, Contract, Event
from settings_test import *


@pytest.fixture
def create_user():
    user = User.objects.create(username='testuser', email='testuser@example.com')
    user.set_password('testpassword')
    user.save()
    return user


@pytest.fixture
def create_client():
    client = Client.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        company='Example Company'
    )
    return client


@pytest.fixture
def create_contract(create_user, create_client):
    contract = Contract.objects.create(
        sales_contact=create_user,
        client=create_client,
        status=False,
        amount=1000
    )
    return contract


@pytest.fixture
def create_event(create_user, create_client):
    event = Event.objects.create(
        client=create_client,
        support_contact=create_user,
        eventStatus='1',
        attendes=10,
        eventDate='2023-05-15',
        note='Example note'
    )
    return event


@pytest.mark.django_db
class TestClientViewSet(TestCase):
    def test_create_client(self):
        url = reverse('clients-list')  # Utilisez le nom de route correct
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'company': 'Example Company'
        }

        response = self.client.post(url, data)
        assert response.status_code == 201
        assert response.data['message'] == 'Client created.'



#     def test_update_client(self, create_user, create_client):
#         url = reverse('client-detail', args=[create_client.client_id])
#         data = {
#             'first_name': 'Updated',
#             'last_name': 'Client',
#             'email': 'updated.client@example.com',
#             'phone': '9876543210',
#             'company': 'Updated Company'
#         }
#
#         self.client.force_login(create_user)
#         response = self.client.put(url, data)
#         assert response.status_code == 200
#         assert response.data['message'] == 'The client has been updated'
#         # Ajoutez d'autres assertions pour vérifier les résultats attendus
#
#     def test_delete_client(self, create_user, create_client):
#         url = reverse('client-detail', args=[create_client.client_id])
#
#         self.client.force_login(create_user)
#         response = self.client.delete(url)
#         assert response.status_code == 204
#         # Vérifiez que le client a été supprimé de la base de données
#
#
# @pytest.mark.django_db
# class TestContractViewSet(TestCase):
#     def test_create_contract(self, create_user, create_client):
#         url = reverse('contract-list', args=[create_client.client_id])
#         data = {
#             'sales_contact': create_user.id,
#             'status': False,
#             'amount': 1500
#         }
#
#         self.client.force_login(create_user)
#         response = self.client.post(url, data)
#         assert response.status_code == 201
#         assert response.data['message'] == 'Job done.'
#         # Ajoutez d'autres assertions pour vérifier les résultats attendus
#
#     def test_update_contract(self, create_user, create_contract):
#         url = reverse('contract-detail', args=[create_contract.client_id,
#                                                create_contract.contract_id])
#         data = {'status': True, 'paymentDue': '2023-05-20'}
#         self.client.force_login(create_user)
#         response = self.client.patch(url, data)
#         assert response.status_code == 200
#         assert response.data['message'] == 'Job done.'
#         # Ajoutez d'autres assertions pour vérifier les résultats attendus
#
#     def test_delete_contract(self, create_user, create_contract):
#         url = reverse('contract-detail', args=[create_contract.client_id, create_contract.contract_id])
#
#         self.client.force_login(create_user)
#         response = self.client.delete(url)
#         assert response.status_code == 204
#         # Vérifiez que le contrat a été supprimé de la base de données
#
#
# @pytest.mark.django_db
# class TestEventViewSet(TestCase):
#     def test_create_event(self, create_user, create_client):
#         url = reverse('event-list', args=[create_client.client_id])
#         data = {
#             'support_contact': create_user.id,
#             'eventStatus': '1',
#             'attendes': 20,
#             'eventDate': '2023-05-25',
#             'note': 'Test event'
#         }
#         self.client.force_login(create_user)
#         response = self.client.post(url, data)
#         assert response.status_code == 201
#         assert response.data['message'] == 'Event created successfully.'
#         # Ajoutez d'autres assertions pour vérifier les résultats attendus
#
#     def test_update_event(self, create_user, create_event):
#         url = reverse('event-detail', args=[create_event.event_id])
#         data = {
#             'support_contact': create_user.id,
#             'eventStatus': '2',
#             'attendes': 30,
#             'eventDate': '2023-05-30',
#             'note': 'Updated event'
#         }
#
#         self.client.force_login(create_user)
#         response = self.client.patch(url, data)
#         assert response.status_code == 200
#         assert response.data['message'] == 'Event updated successfully.'
#         # Ajoutez d'autres assertions pour vérifier les résultats attendus
#
#     def test_delete_event(self, create_user, create_event):
#         url = reverse('event-detail', args=[create_event.event_id])
#
#         self.client.force_login(create_user)
#         response = self.client.delete(url)
#         assert response.status_code == 204
#         # Vérifiez que l'événement a été supprimé de la base de données
