import pytest

from common.errors import InvalidCredentials
from services.auth import AuthService
from tests.factories import UserFactory


@pytest.mark.django_db
def test_login_successful():
    # given
    new_user = UserFactory()

    # when
    auth_service = AuthService()
    user = auth_service.login(username=new_user.username, password='testpass123')

    # then
    assert user == new_user
    assert user.email == new_user.email
    assert user.username == new_user.username


@pytest.mark.django_db
def test_login_failed_user_does_not_exist():
    # given
    # no user

    # when & then
    auth_service = AuthService()
    with pytest.raises(InvalidCredentials):
        user = auth_service.login(username='bob', password='testpass123')  # noqa: F841


@pytest.mark.django_db
def test_login_failed_invalid_password():
    # given
    new_user = UserFactory()

    # when & then
    auth_service = AuthService()
    with pytest.raises(InvalidCredentials):
        user = auth_service.login(username=new_user.username, password='invalid_password')  # noqa: F841
