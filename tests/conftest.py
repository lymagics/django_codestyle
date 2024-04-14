import pytest
from faker import Faker
from rest_framework.test import APIClient


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
