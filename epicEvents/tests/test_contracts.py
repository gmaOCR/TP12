from datetime import datetime

import pytest, json
from django.contrib.auth import get_user_model
from rest_framework import status

from sales.models import Client, Contract, Event
from sales.views import ClientViewSet, ContractViewSet, EventViewSet

User = get_user_model()


@pytest.mark.django_db
def test_create_anonyme(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/'
    data = {
        'amount': 100.0,
        'status': True,
        'paymentDue': "2002-02-02"
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
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
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
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    data = {
        'amount': 200.0,
        'status': True,
        'paymentDue': "2002-02-02"
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
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_get_user(api_client, vente_user):
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
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_other_user(api_client, vente_user, vente_user_2):
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
    api_client.force_authenticate(user=vente_user_2)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_contract_as_vente(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/'
    data = {
        'amount': 100.0,
        'status': True,
        'paymentDue': "2002-02-02"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1
    assert Contract.objects.count() == 1


@pytest.mark.django_db
def test_create_contract_as_gestion(api_client, gestion_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=gestion_user
    )
    api_client.force_authenticate(user=gestion_user)
    url = f'/api/client/{client.client_id}/contract/'
    data = {
        'amount': 100.0,
        'status': True,
        'paymentDue': "2002-02-02"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1
    assert Contract.objects.count() == 1


@pytest.mark.django_db
def test_update_contract_as_vente(api_client, vente_user):
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
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    data = {
        'amount': 200.0,
        'status': True,
        'paymentDue': "2002-02-02"
    }
    response = api_client.put(url, data)
    contract.refresh_from_db()
    assert contract.status is True
    assert contract.paymentDue == datetime.strptime("2002-02-02", "%Y-%m-%d").date()
    assert contract.amount == 200.0
    assert response.status_code == status.HTTP_200_OK


def test_update_contract_as_gestion_not_owner(api_client, vente_user, gestion_user):
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
    api_client.force_authenticate(user=gestion_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    data = {
        'amount': 200.0,
        'status': True,
        'paymentDue': "2002-02-02"
    }
    response = api_client.put(url, data)
    contract.refresh_from_db()
    assert contract.status is True
    assert contract.paymentDue == datetime.strptime("2002-02-02", "%Y-%m-%d").date()
    assert contract.amount == 200.0
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_contract_not_signed(api_client, vente_user):
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
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    data = {
        'status': False,
        'paymentDue': "2002-02-02"
    }
    response = api_client.put(url, data)
    contract.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert contract.status is False
    assert contract.paymentDue is None
    assert response.data[0] == "Contract must be signed to have a payment date value"


@pytest.mark.django_db
def test_update_payement_due_null_status_true(api_client, vente_user):
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
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    data = {
        'paymentDue': ""
    }
    response = api_client.put(url, data)
    contract.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'message': {'paymentDue': ['Payment due must be set if the status is signed.']}}


@pytest.mark.django_db
def test_update_contract_other_user(api_client, vente_user, vente_user_2):
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
    api_client.force_authenticate(user=vente_user_2)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    data = {
        'amount': 200.0,
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_contract_as_vente(api_client, vente_user):
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
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Contract.objects.count() == 1


@pytest.mark.django_db
def test_delete_contract_as_gestion(api_client, gestion_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=gestion_user
    )
    contract = Contract.objects.create(
        client=client,
        sales_contact=gestion_user,
        amount=100.0,
    )
    api_client.force_authenticate(user=gestion_user)
    url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Contract.objects.count() == 0
