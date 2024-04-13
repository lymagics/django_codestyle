from urllib.parse import urlencode

from django.urls import reverse

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import PostFactory, UserFactory


@pytest.mark.django_db
def test_post_create_successful(fake: Faker, api_client: APIClient):
    # given
    user = UserFactory()
    request_data = {'text': fake.sentence()}

    # when
    url = reverse('posts_create')
    api_client.force_authenticate(user)
    response = api_client.post(url, request_data)

    # then
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert 'text' in response_data
    assert response_data['text'] == request_data['text']
    assert 'created_at' in response_data
    assert 'author' in response_data
    assert response_data['author']['username'] == user.username


@pytest.mark.django_db
def test_get_post_by_id_successful(api_client: APIClient):
    # given
    user = UserFactory()
    post = PostFactory(author=user)

    # when
    url = reverse('posts_get', kwargs={'id': post.id})
    api_client.force_authenticate(user)
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert 'id' in response_data
    assert response_data['id'] == post.id
    assert 'text' in response_data
    assert response_data['text'] == post.text
    assert 'author' in response_data
    assert response_data['author']['username'] == user.username
    assert 'created_at' in response_data


@pytest.mark.django_db
def test_get_post_by_id_fail_post_does_not_exist(api_client: APIClient):
    # given
    user = UserFactory()

    # when
    url = reverse('posts_get', kwargs={'id': 1})
    api_client.force_authenticate(user)
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_post_by_id_fail_unauthenticated(api_client: APIClient):
    # given
    post = PostFactory()

    # when
    url = reverse('posts_get', kwargs={'id': post.id})
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_posts_list_successful(api_client: APIClient):
    # given
    user = UserFactory()
    post = PostFactory(author=user)

    # when
    url = reverse('posts_list')
    api_client.force_authenticate(user)
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert 'pagination' in response_data
    assert 'count' in response_data['pagination']
    assert 'limit' in response_data['pagination']
    assert 'offset' in response_data['pagination']
    assert response_data['pagination']['count'] == 1
    assert response_data['pagination']['limit'] == 10
    assert response_data['pagination']['offset'] == 0
    assert 'posts' in response_data
    assert len(response_data['posts']) == 1
    assert 'text' in response_data['posts'][0]
    assert response_data['posts'][0]['text'] == post.text


@pytest.mark.django_db
def test_get_posts_list_fail_invalid_pagination(api_client: APIClient):
    # given
    user = UserFactory()

    # when
    qs = urlencode({'limit': -1, 'offset': -1})
    url = reverse('posts_list')
    api_client.force_authenticate(user)
    response = api_client.get(url + '?' + qs)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert 'limit' in response_data
    assert 'offset' in response_data
    assert response_data['limit'] == ['Ensure this value is greater than or equal to 0.']
    assert response_data['offset'] == ['Ensure this value is greater than or equal to 0.']


@pytest.mark.django_db
def test_get_posts_list_fail_unauthenticated(api_client: APIClient):
    # given
    # no user

    # when
    url = reverse('posts_list')
    response = api_client.get(url)

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
