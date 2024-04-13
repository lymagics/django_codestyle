from django.contrib.auth import authenticate

from common.errors import InvalidCredentials
from database.models.user import User


class AuthService:
    """
    Auth service.
    """
    def login(self, username: str, password: str) -> User:
        user = authenticate(username=username, password=password)
        if user is None:
            error = 'Invalid username or password.'
            raise InvalidCredentials(error)
        return user
