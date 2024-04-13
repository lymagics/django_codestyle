import pytest
from faker import Faker

from database.models.user import User
from services.user import UsersService
from tests.factories import UserFactory


@pytest.mark.django_db
def test_create_user(fake: Faker):
    # given
    assert User.objects.count() == 0

    # when
    users_service = UsersService()
    new_user = users_service.create(
        email=fake.email(),
        username=fake.user_name(),
        password='testpass123',
    )

    # then
    assert User.objects.count() == 1

    user = User.objects.first()
    assert user == new_user
    assert user.email == new_user.email
    assert user.username == new_user.username


@pytest.mark.django_db
def test_get_user_by_id():
    # given
    new_user = UserFactory(id=1)

    # when
    users_service = UsersService()
    user = users_service.get_by_id(id=1)

    # then
    assert user is not None
    assert user == new_user
    assert user.email == new_user.email
    assert user.username == new_user.username
