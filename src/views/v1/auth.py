from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from common.errors import InvalidCredentials
from schemas.request.credentials import CredentialsIn
from services.auth import AuthService
from services.jwt import JwtService


@api_view(['POST'])
def login(request: Request) -> Response:
    schema = CredentialsIn(data=request.data)
    schema.is_valid(raise_exception=True)

    try:
        auth_service = AuthService()
        user = auth_service.login(**schema.validated_data)
    except InvalidCredentials as e:
        detail = {'detail': str(e)}
        return Response(detail, status=status.HTTP_401_UNAUTHORIZED)

    jwt_service = JwtService()
    jwt_token = jwt_service.encode({'user_id': user.id})

    return Response({'token': jwt_token}, status=status.HTTP_200_OK)


urlpatterns = [
    path('login/', login, name='auth_login'),
]
