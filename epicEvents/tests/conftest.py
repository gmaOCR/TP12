import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from sales.models import Contract, Client, Event


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def vente_user(db):
    User = get_user_model()
    username = 'vente_user'
    password = 'password'
    role = 'vente'
    user = User.objects.create_user(username=username, role=role, password=password)
    yield user
    user.delete()

@pytest.fixture
def vente_user_2(db):
    User = get_user_model()
    username = 'vente_user_2'
    password = 'password'
    role = 'vente'
    user = User.objects.create_user(username=username, role=role, password=password)
    yield user
    user.delete()


@pytest.fixture
def support_user(db):
    User = get_user_model()
    username = 'support_user'
    password = 'password'
    role = 'support'
    user = User.objects.create_user(username=username, role=role, password=password)
    yield user
    user.delete()

@pytest.fixture
def support_user_2(db):
    User = get_user_model()
    username = 'support_user_2'
    password = 'password'
    role = 'support'
    user = User.objects.create_user(username=username, role=role, password=password)
    yield user
    user.delete()

@pytest.fixture
def gestion_user(db):
    User = get_user_model()
    username = 'gestion_user'
    password = 'password'
    role = 'Gestion'
    user = User.objects.create_user(username=username, role=role, password=password)
    yield user
    user.delete()


@pytest.fixture
def test_data(vente_user, support_user):
    client = Client.objects.create(
        last_name='toto',
        email='tata@none.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    client2 = Client.objects.create(
        last_name='tata',
        email='toto@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    contract = Contract(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    contract2 = Contract(
        sales_contact=vente_user,
        client=client2,
        amount=1000.0
    )
    event = Event.objects.create(
        client=contract.client,
        eventStatus="1",
        attendes=10,
        eventDate='2023-01-01',
        note='Event note',
        support_contact=support_user
    )
    event2 = Event.objects.create(
        client=contract2.client,
        eventStatus="2",
        attendes=20,
        eventDate='2023-01-02',
        note='Event note',
        support_contact=support_user
    )
    contract.save()
    contract2.save()

    return {
        'client': client,
        'client2': client2,
        'contract': contract,
        'contract2': contract2,
        'event': event,
        'event2': event2,
    }
