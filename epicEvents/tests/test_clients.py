import pytest, json
from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework import status

from sales.models import Client, Contract, Event
from sales.views import ClientViewSet, ContractViewSet, EventViewSet

User = get_user_model()


@pytest.mark.django_db
def test_create_client(api_client, vente_user):
    api_client.force_authenticate(user=vente_user)
    url = '/api/clients/'
    data = {
        'email': 'client@example.com',
        'phone': '1234567890',
        'company': "Name",
        'sales_contact': vente_user.username,
        'first_name': 'John',
        'last_name': 'Doe',
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Client.objects.count() == 1


@pytest.mark.django_db
def test_update_client(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/clients/{client.client_id}/'
    data = {
        'email': 'updated_client@example.com',
        'phone': '9876543210',
        'company': "Updated Company",
        'sales_contact': vente_user,
        'first_name': 'Joohn',
        'last_name': 'Doe',
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Client.objects.get(pk=client.pk).first_name == 'Joohn'


@pytest.mark.django_db
def test_create_contract(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/clients/{client.client_id}/contracts/'
    data = {
        'amount': 100.0,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Contract.objects.count() == 1


@pytest.mark.django_db
def test_update_client_other_user(api_client, vente_user, vente_user_2):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user_2)
    url = f'/api/clients/{client.client_id}/'
    data = {
        'email': 'updated_client@example.com',
        'phone': '9876543210',
        'company': "Updated Company",
        'sales_contact': vente_user.username,
        'first_name': 'Joohn',
        'last_name': 'Doe',
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_client_as_vente(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/clients/{client.client_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Client.objects.count() == 1


@pytest.mark.django_db
def test_delete_client_as_gestion(api_client, vente_user, gestion_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=gestion_user)
    url = f'/api/clients/{client.client_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Client.objects.count() == 0
