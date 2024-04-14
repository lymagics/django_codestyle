from django.db import transaction
from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.auth import TokenAuthentication
from schemas.request.user import UserIn
from schemas.response.user import UserOut
from services.user import UsersService
from services.mail import MailService


@api_view(['POST'])
def create_user(request: Request) -> Response:
    schema = UserIn(data=request.data)
    schema.is_valid(raise_exception=True)

    with transaction.atomic():
        users_service = UsersService()
        user = users_service.create(**schema.validated_data)
        mail_service = MailService()
        mail_service.send_greetings_email(user=user)

    schema = UserOut(user)
    return Response(schema.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_me(request: Request) -> Response:
    schema = UserOut(request.user)
    return Response(schema.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_id(request: Request, id: int) -> Response:
    users_service = UsersService()
    user = users_service.get_by_id(id=id)

    if user is None:
        detail = {'detail': 'User not found.'}
        return Response(detail, status=status.HTTP_404_NOT_FOUND)
    schema = UserOut(user)
    return Response(schema.data, status=status.HTTP_200_OK)


urlpatterns = [
    path('create/', create_user, name='users_create'),
    path('me/', get_me, name='users_me'),
    path('<int:id>/', get_user_by_id, name='users_get'),
]
