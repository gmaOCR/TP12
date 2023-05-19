from freezegun import freeze_time
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from sales.models import Client, Contract, Event

User = get_user_model()
freeze = "2023-05-18"


@pytest.mark.django_db
@freeze_time(freeze)
def test_search_endpoints(api_client, vente_user, support_user):
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
        eventDate='2023-01-01',
        note='Event note',
        support_contact=support_user
    )
    contract.save()

    api_client.force_authenticate(user=support_user)

    url = f'/api/clients/?email=example.com'
    response = api_client.get(url)
    email = len(response.data)

    url = f'/api/clients/?last_name=tata'
    response = api_client.get(url)
    last_name = len(response.data)

    url = f'/api/contracts/?dateCreated={freeze}'
    response = api_client.get(url)
    datecreated = len(response.data)

    contract2.save()  # continue contract test with 2 obj in DB

    url = f'/api/contracts/?client_email=example'
    response = api_client.get(url)
    client_email = len(response.data)

    url = f'/api/contracts/?client_last_name=tata'
    response = api_client.get(url)
    client_last_name = len(response.data)

    url = f'/api/contracts/?amount=100'
    response = api_client.get(url)
    amount = len(response.data)

    url_events = f'/api/events/?search='
    response_event = api_client.get(url_events)

    # All objects count 2 in DB, if assert == 1 , test is valid
    # Clients assert
    assert email == 1
    assert last_name == 1

    # Contracts assert
    assert amount == 1
    assert datecreated == 1  # only one contract saved so dateCreated updated based on "freezed time"
    assert client_email == 1
    assert client_last_name == 1

    # Events assert
