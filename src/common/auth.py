from rest_framework import authentication
from rest_framework.request import Request

from services.jwt import JwtService
from services.user import UsersService


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Token Authentication class.
    """
    def authenticate(self, request: Request):
        token = request.META.get('HTTP_JWT')
        if token is None:
            return None

        jwt_service = JwtService()
        payload = jwt_service.decode(token)
        if payload is None or 'user_id' not in payload:
            return None

        users_service = UsersService()
        user = users_service.get_by_id(payload['user_id'])
        return (user, None)
