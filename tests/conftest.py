import secrets

import pytest
from faker import Faker
from rest_framework.test import APIClient


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture
def fake_secret_key() -> str:
    return secrets.token_urlsafe(16)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
