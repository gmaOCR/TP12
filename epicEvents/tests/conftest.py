import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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
