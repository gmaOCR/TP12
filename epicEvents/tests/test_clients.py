import pytest, json
from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework import status

from sales.models import Client, Contract, Event

User = get_user_model()


@pytest.mark.django_db
def test_create_anonyme(api_client, vente_user):
    api_client.force_authenticate(user=None)
    url = f'/api/client/'
    data = {
        'email': "client@example.com",
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
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/'
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
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/'
    data = {
        'phone': "054504"
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
    api_client.force_authenticate(user=None)
    url = f'/api/client/{client.client_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_get(api_client, vente_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user)
    url = f'/api/client/{client.client_id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_other_user(api_client, vente_user, support_user):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=support_user)
    url = f'/api/client/{client.client_id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_client_as_vente_user(api_client, vente_user):
    api_client.force_authenticate(user=vente_user)
    url = '/api/client/'
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
def test_create_client_as_gestion_user(api_client, gestion_user):
    api_client.force_authenticate(user=gestion_user)
    url = '/api/client/'
    data = {
        'email': 'client@example.com',
        'phone': '1234567890',
        'company': "Name",
        'sales_contact': gestion_user.username,
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
    url = f'/api/client/{client.client_id}/'
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
    assert Client.objects.get(pk=client.client_id).first_name == 'Joohn'


@pytest.mark.django_db
def test_update_client_other_user(api_client, vente_user, vente_user_2):
    client = Client.objects.create(
        email='client@example.com',
        phone='1234567890',
        company='Company',
        sales_contact=vente_user
    )
    api_client.force_authenticate(user=vente_user_2)
    url = f'/api/client/{client.client_id}/'
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
    url = f'/api/client/{client.client_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == "You are not authorized to perform this action (Manager)."
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
    url = f'/api/client/{client.client_id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data['message'] == "The client has been deleted"
    assert Client.objects.count() == 0
