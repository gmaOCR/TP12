from datetime import datetime

import pytest, json
from django.contrib.auth import get_user_model
from rest_framework import status

from sales.models import Client, Contract, Event


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
    assert response.status_code == status.HTTP_200_OK
    assert event.eventStatus == "2"
    assert event.note == "new note"
#
#
# @pytest.mark.django_db
# def test_update_event_by_support_user(api_client, vente_user, support_user):
#     client = Client.objects.create(
#         email='client@example.com',
#         phone='1234567890',
#         company='Company',
#         sales_contact=vente_user
#     )
#     contract = Contract.objects.create(
#         sales_contact=vente_user,
#         client=client,
#         amount=100.0
#     )
#     event = Event.objects.create(
#         client=contract.client,
#         eventStatus="1",
#         attendes=10,
#         eventDate='2023-01-01',
#         note='Event note',
#         support_contact=support_user
#     )
#     api_client.force_authenticate(user=support_user)
#     url = f'/api/client/{client.client_id}/contract/{contract.contract_id}/event/{event.event_id}/'
#     data = {
#         'note': "new note",
#         'eventStatus': "2",
#         'attendes': 100
#     }
#     response = api_client.put(url, data)
#     event.refresh_from_db()
#     assert event.eventStatus == "2"
#     assert event.note == "new note"
#     assert response.status_code == status.HTTP_200_OK