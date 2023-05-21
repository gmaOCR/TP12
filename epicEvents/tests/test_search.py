from freezegun import freeze_time
import pytest
from django.contrib.auth import get_user_model

from sales.models import Client, Contract, Event

User = get_user_model()
freeze = "2023-05-18"


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
    contract = Contract.objects.create(
        sales_contact=vente_user,
        client=client,
        amount=100.0
    )
    contract2 = Contract.objects.create(
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

    return {
        'client': client,
        'client2': client2,
        'contract': contract,
        'contract2': contract2,
        'event': event,
        'event2': event2,
        'vente_user': vente_user,
        'support_user': support_user,
    }


@pytest.mark.django_db
class TestSearchEndpoints:

    def test_search_by_email(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/clients/?email=example.com'
        response = api_client.get(url)
        email = len(response.data)

        assert email == 1

    def test_search_by_last_name(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/clients/?last_name=tata'
        response = api_client.get(url)
        last_name = len(response.data)

        assert last_name == 1

    @freeze_time(freeze)
    def test_search_by_date_created(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        # Save a new Contract instance to update the dateCreated field
        new_contract = Contract(
            sales_contact=test_data['vente_user'],
            client=test_data['client'],
            amount=200.0
        )
        new_contract.save()

        url = f'/api/contracts/?dateCreated={freeze}'
        response = api_client.get(url)
        date_created = len(response.data)

        assert date_created == 1

    def test_search_by_client_email(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?client_email=example'
        response = api_client.get(url)
        client_email = len(response.data)

        assert client_email == 1

    def test_search_by_client_last_name(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?client_last_name=tata'
        response = api_client.get(url)
        client_last_name = len(response.data)

        assert client_last_name == 1

    def test_search_by_amount(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?amount=100'
        response = api_client.get(url)
        amount = len(response.data)

        assert amount == 1

    def test_search_by_event_client_last_name(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/events/?client_last_name=tata'
        response = api_client.get(url)
        client_last_name_event = len(response.data)

        assert client_last_name_event == 1

    def test_search_by_event_client_mail(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/events/?client_email=example'
        response = api_client.get(url)
        client_email_event = len(response.data)

        assert client_email_event == 1

    def test_search_by_event_date(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/events/?eventDate=2023-01-02'
        response = api_client.get(url)
        event_date = len(response.data)

        assert event_date == 1


@pytest.mark.django_db
class TestSearchEmptyEndpoints:
    @freeze_time(freeze)
    def test_search_by_email(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/clients/?email='
        response = api_client.get(url)
        email = len(response.data)

        assert email == 2

    @freeze_time(freeze)
    def test_search_by_last_name(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/clients/?last_name='
        response = api_client.get(url)
        last_name = len(response.data)

        assert last_name == 2

    @freeze_time(freeze)
    def test_search_by_date_created(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?dateCreated='
        response = api_client.get(url)
        date_created = len(response.data)

        assert date_created == 2

    @freeze_time(freeze)
    def test_search_by_client_email(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?client_email='
        response = api_client.get(url)
        client_email = len(response.data)

        assert client_email == 2

    @freeze_time(freeze)
    def test_search_by_client_last_name(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?client_last_name='
        response = api_client.get(url)
        client_last_name = len(response.data)

        assert client_last_name == 2

    @freeze_time(freeze)
    def test_search_by_amount(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/contracts/?amount='
        response = api_client.get(url)
        amount = len(response.data)

        assert amount == 2

    @freeze_time(freeze)
    def test_search_by_event_client_last_name(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/events/?client_last_name='
        response = api_client.get(url)
        client_last_name_event = len(response.data)

        assert client_last_name_event == 2

    @freeze_time(freeze)
    def test_search_by_event_client_email(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/events/?client_email='
        response = api_client.get(url)
        client_email_event = len(response.data)

        assert client_email_event == 2

    @freeze_time(freeze)
    def test_search_by_event_date(self, api_client, test_data):
        api_client.force_authenticate(user=test_data['support_user'])

        url = '/api/events/?eventDate='
        response = api_client.get(url)
        event_date = len(response.data)

        assert event_date == 2