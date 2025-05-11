"""Fixtures for testing of application common."""
import pytest
from django.test.client import Client
from django.urls import reverse
from erp_model import settings


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create_user(
        username='erp_user_1',
        password='ERP_USER_1_PASSWORD'
    )


@pytest.fixture
def user_client(auth_user):
    user_client = Client()
    user_client.force_login(auth_user)
    return user_client


@pytest.fixture
def anonymous_client(client):
    return client


@pytest.fixture
def url_home():
    return reverse('common:index')


@pytest.fixture
def url_currency_list():
    return reverse('common:currency_list')


@pytest.fixture
def url_users_login():
    return settings.LOGIN_URL


@pytest.fixture
def url_users_logout():
    return reverse('users:logout')


@pytest.fixture
def url_users_signup():
    return reverse('users:signup')
