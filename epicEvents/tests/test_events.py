import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from sales.models import Client, Contract, Event

User = get_user_model()


@pytest.mark.django_db
def test_create_anonyme(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/'
    data = {
        'client': contract.client,
        'eventStatus': '1',
        'attendes': 10,
        'eventDate': '2023-01-01',
        'note': 'Event note'
    }
    response = api_client.post(url, data)
    assert response.data['detail'] == 'Authentication credentials were not provided.'
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_read_anonyme(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_update_anonyme(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    data = {
        'note': "new note",
        'eventStatus': "2",
        'attendes': 100
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_delete_anonyme(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        client=client,
        sales_contact=vente_user,
        amount=100.0,
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_read_user(api_client, vente_user, support_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note',
        support_contact=support_user
    )
    api_client.force_authenticate(user=support_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    api_client.force_authenticate(user=vente_user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_event(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0,
        status=True
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/'
    data = {
        'client': contract.client,
        'eventStatus': '1',
        'attendes': 10,
        'eventDate': '2023-01-01',
        'note': 'Event note'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_create_event_contract_status_false(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0,
        status=False
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/'
    data = {
        'client': contract.client,
        'eventStatus': '1',
        'attendes': 10,
        'eventDate': '2023-01-01',
        'note': 'Event note'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "The specified contract does not exist or its status is False."


@pytest.mark.django_db
def test_update_event_by_vente_user_client_creator(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    data = {
        'note': "new note",
        'eventStatus': "2",
        'attendes': 100
    }
    response = api_client.put(url, data)
    event.refresh_from_db()
    assert event.eventStatus == "2"
    assert event.note == "new note"
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_event_by_other_vente_user(api_client, vente_user, vente_user_2):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=vente_user_2)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    data = {
        'note': "new note",
        'eventStatus': "2",
        'attendes': 100
    }
    response = api_client.put(url, data)
    event.refresh_from_db()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == " You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_event_by_support_user(api_client, vente_user, support_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note',
        support_contact=support_user
    )
    api_client.force_authenticate(user=support_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    data = {
        'note': "new note",
        'eventStatus': "2",
        'attendes': 100
    }
    response = api_client.put(url, data)
    event.refresh_from_db()
    assert event.eventStatus == "2"
    assert event.note == "new note"
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_event_by_other_support(api_client, vente_user, support_user, support_user_2):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note',
        support_contact=support_user
    )
    api_client.force_authenticate(user=support_user_2)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    data = {
        'note': "new note",
        'eventStatus': "2",
        'attendes': 100
    }
    response = api_client.put(url, data)
    event.refresh_from_db()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == " You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_as_vente_user(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        client=client,
        sales_contact=vente_user,
        amount=100.0,
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_delete_as_gestion_user(api_client, vente_user, gestion_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract.objects.create(
        client=client,
        sales_contact=vente_user,
        amount=100.0,
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note'
    )
    api_client.force_authenticate(user=gestion_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Event.objects.count() == 0
