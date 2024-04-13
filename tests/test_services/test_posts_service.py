import pytest
from faker import Faker

from database.models.post import Post
from services.post import PostsService
from tests.factories import PostFactory, UserFactory


@pytest.mark.django_db
def test_create_post(fake: Faker):
    # given
    author = UserFactory()
    assert Post.objects.count() == 0

    # when
    posts_service = PostsService()
    new_post = posts_service.create(text=fake.sentence(), author=author)

    # then
    assert Post.objects.count() == 1

    post = Post.objects.first()
    assert post == new_post
    assert post.text == new_post.text
    assert post.author == author


@pytest.mark.django_db
def test_get_post_by_id():
    # given
    new_post = PostFactory(id=1)

    # when
    posts_service = PostsService()
    post = posts_service.get_by_id(id=1)

    # then
    assert post is not None
    assert post == new_post
    assert post.text == new_post.text
    assert post.author == new_post.author


@pytest.mark.django_db
def test_get_posts_list():
    # given
    post = PostFactory()
    another_post = PostFactory()

    # when
    posts_service = PostsService()
    posts = posts_service.get_list(limit=10, offset=0)

    # then
    assert len(posts) == 2
    assert post in posts
    assert another_post in posts


@pytest.mark.django_db
def test_post_count():
    # given
    post = PostFactory()  # noqa: F841
    another_post = PostFactory()  # noqa: F841

    # when
    posts_service = PostsService()
    posts_count = posts_service.get_count()

    # then
    assert posts_count == 2
