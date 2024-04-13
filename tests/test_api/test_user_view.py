from django.urls import reverse

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from pytest_mock import MockerFixture

from tests.factories import UserFactory


@pytest.mark.django_db
def test_user_create_successful(mocker: MockerFixture, fake: Faker, api_client: APIClient):
    # given
    request_data = {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': 'testpass123',
    }
    mock_send_greetings_email = mocker.patch('views.user.MailService.send_greetings_email')

    # when
    url = reverse('users_create')
    response = api_client.post(url, request_data)

    # then
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert 'avatar_url' in response_data
    assert 'username' in response_data
    assert 'email' not in response_data
    assert request_data['username'] == response_data['username']

    mock_send_greetings_email.assert_called_once()


@pytest.mark.django_db
def test_user_create_fail_email_already_in_user(fake: Faker, api_client: APIClient):
    # given
    user = UserFactory()
    request_data = {
        'email': user.email,
        'username': fake.user_name(),
        'password': 'testpass123',
    }

    # when
    url = reverse('users_create')
    response = api_client.post(url, request_data)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert 'email' in response_data
    assert response_data['email'] == ['user with this email already exists.']


@pytest.mark.django_db
def test_user_create_fail_username_already_in_user(fake: Faker, api_client: APIClient):
    # given
    user = UserFactory()
    request_data = {
        'email': fake.email(),
        'username': user.username,
        'password': 'testpass123',
    }

    # when
    url = reverse('users_create')
    response = api_client.post(url, request_data)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert 'username' in response_data
    assert response_data['username'] == ['A user with that username already exists.']


@pytest.mark.django_db
def test_get_user_by_id_sucessful(api_client: APIClient):
    # given
    user = UserFactory()

    # when
    url = reverse('users_get', kwargs={'id': user.id})
    api_client.force_authenticate(user)
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['username'] == user.username
    assert response_data['id'] == user.id


@pytest.mark.django_db
def test_get_user_by_id_fail_user_does_not_exist(api_client: APIClient):
    # given
    user = UserFactory()

    # when
    url = reverse('users_get', kwargs={'id': 2})
    api_client.force_authenticate(user)
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_user_by_id_fail_unauthenticated(api_client: APIClient):
    # given
    user = UserFactory()

    # when
    url = reverse('users_get', kwargs={'id': user.id})
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_authenticated_user_successful(api_client: APIClient):
    # given
    user = UserFactory()

    # when
    url = reverse('users_me')
    api_client.force_authenticate(user)
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['username'] == user.username
    assert response_data['id'] == user.id


@pytest.mark.django_db
def test_get_authenticated_user_fail_unauthenticated(api_client: APIClient):
    # given
    user = UserFactory()  # noqa: F841

    # when
    url = reverse('users_me')
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
