from django.urls import reverse

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.mark.django_db
def test_login_successful(api_client: APIClient):
    # given
    user = UserFactory()
    request_data = {
        'username': user.username,
        'password': 'testpass123',
    }

    # when
    url = reverse('auth_login')
    response = api_client.post(url, request_data)

    # then
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert 'token' in response_data


@pytest.mark.django_db
def test_login_fail_invalid_credentials(fake: Faker, api_client: APIClient):
    # given
    request_data = {
        'username': fake.user_name(),
        'password': 'invalid_password',
    }

    # when
    url = reverse('auth_login')
    response = api_client.post(url, request_data)

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
