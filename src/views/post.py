from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.auth import TokenAuthentication
from schemas.request.pagination import PaginationIn
from schemas.request.post import PostIn
from schemas.response.post import PostOut
from services.post import PostsService


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request: Request) -> Response:
    schema = PostIn(data=request.data)
    schema.is_valid(raise_exception=True)

    posts_service = PostsService()
    post = posts_service.create(author=request.user, **schema.validated_data)

    schema = PostOut(post)
    return Response(schema.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_post_by_id(request: Request, id: int) -> Response:
    posts_service = PostsService()
    post = posts_service.get_by_id(id=id)

    if post is None:
        detail = {'detail': 'Post not found.'}
        return Response(detail, status=status.HTTP_404_NOT_FOUND)
    schema = PostOut(post)
    return Response(schema.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_posts_list(request: Request) -> Response:
    schema = PaginationIn(data=request.query_params)
    schema.is_valid(raise_exception=True)

    posts_service = PostsService()
    posts = posts_service.get_list(**schema.validated_data)
    count = posts_service.get_count()

    response = {
        'pagination': {
            'count': count,
            **schema.validated_data,
        },
        'posts': PostOut(posts, many=True).data,
    }
    return Response(response, status=status.HTTP_200_OK)


urlpatterns = [
    path('create/', create_post, name='posts_create'),
    path('<int:id>/', get_post_by_id, name='posts_get'),
    path('', get_posts_list, name='posts_list'),
]
