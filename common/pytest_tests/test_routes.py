"""Module for testing routes of common application."""
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client, status',
    [
        (
            pytest.lazy_fixture('url_home'),
            'client',
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_currency_list'),
            pytest.lazy_fixture('user_client'),
            HTTPStatus.OK),
    ],
    indirect=['client']
)
def test_pages_availability(url, client, status, url_users_login):
    response = client.get(url)
    if response.status_code == HTTPStatus.FOUND:  # 302 Redirect
        expected_url = f'{url_users_login}?next={url}'
        assertRedirects(response, expected_url)
    else:
        assert response.status_code == status
